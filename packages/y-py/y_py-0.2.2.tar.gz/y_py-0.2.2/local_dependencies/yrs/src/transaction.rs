use crate::*;

use crate::block::{BlockPtr, Item, ItemContent, Prelim, ID};
use crate::block_store::{Snapshot, StateVector};
use crate::event::UpdateEvent;
use crate::id_set::DeleteSet;
use crate::store::Store;
use crate::types::array::Array;
use crate::types::xml::{XmlElement, XmlText};
use crate::types::{
    Branch, Map, Text, TypePtr, TYPE_REFS_ARRAY, TYPE_REFS_MAP, TYPE_REFS_TEXT,
    TYPE_REFS_XML_ELEMENT, TYPE_REFS_XML_TEXT,
};
use crate::update::Update;
use std::cell::UnsafeCell;
use std::collections::{HashMap, HashSet};
use std::rc::Rc;
use updates::encoder::*;

/// Transaction is one of the core types in Yrs. All operations that need to touch a document's
/// contents (a.k.a. block store), need to be executed in scope of a transaction.
pub struct Transaction {
    /// Store containing the state of the document.
    store: Rc<UnsafeCell<Store>>,
    /// State vector of a current transaction at the moment of its creation.
    pub before_state: StateVector,
    /// Current state vector of a transaction, which includes all performed updates.
    pub after_state: StateVector,
    /// ID's of the blocks to be merged.
    pub merge_blocks: Vec<ID>,
    /// Describes the set of deleted items by ids.
    pub delete_set: DeleteSet,
    /// All types that were directly modified (property added or child inserted/deleted).
    /// New types are not included in this Set.
    changed: HashMap<TypePtr, HashSet<Option<Rc<str>>>>,
    committed: bool,
}

impl Transaction {
    pub(crate) fn new(store: Rc<UnsafeCell<Store>>) -> Transaction {
        let begin_timestamp = unsafe { (&*store.get()).blocks.get_state_vector() };
        Transaction {
            store,
            before_state: begin_timestamp,
            merge_blocks: Vec::new(),
            delete_set: DeleteSet::new(),
            after_state: StateVector::default(),
            changed: HashMap::new(),
            committed: false,
        }
    }
    pub(crate) fn store(&self) -> &Store {
        unsafe { self.store.get().as_ref().unwrap() }
    }

    pub(crate) fn store_mut(&mut self) -> &mut Store {
        unsafe { self.store.get().as_mut().unwrap() }
    }

    /// Returns state vector describing current state of the updates.
    pub fn state_vector(&self) -> StateVector {
        self.store().blocks.get_state_vector()
    }

    pub fn snapshot(&self) -> Snapshot {
        let blocks = &self.store().blocks;
        let sv = blocks.get_state_vector();
        let ds = DeleteSet::from(blocks);
        Snapshot::new(sv, ds)
    }

    /// Encodes the difference between remove peer state given its `state_vector` and the state
    /// of a current local peer
    pub fn encode_diff<E: Encoder>(&self, state_vector: &StateVector, encoder: &mut E) {
        self.store().encode_diff(state_vector, encoder)
    }

    /// Returns a [Text] data structure stored under a given `name`. Text structures are used for
    /// collaborative text editing: they expose operations to append and remove chunks of text,
    /// which are free to execute concurrently by multiple peers over remote boundaries.
    ///
    /// If not structure under defined `name` existed before, it will be created and returned
    /// instead.
    ///
    /// If a structure under defined `name` already existed, but its type was different it will be
    /// reinterpreted as a text (in such case a sequence component of complex data type will be
    /// interpreted as a list of text chunks).
    pub fn get_text(&mut self, name: &str) -> Text {
        let c = self.store_mut().create_type(name, None, TYPE_REFS_TEXT);
        Text::from(c)
    }

    /// Returns a [Map] data structure stored under a given `name`. Maps are used to store key-value
    /// pairs associated together. These values can be primitive data (similar but not limited to
    /// a JavaScript Object Notation) as well as other shared types (Yrs maps, arrays, text
    /// structures etc.), enabling to construct a complex recursive tree structures.
    ///
    /// If not structure under defined `name` existed before, it will be created and returned
    /// instead.
    ///
    /// If a structure under defined `name` already existed, but its type was different it will be
    /// reinterpreted as a map (in such case a map component of complex data type will be
    /// interpreted as native map).
    pub fn get_map(&mut self, name: &str) -> Map {
        let c = self.store_mut().create_type(name, None, TYPE_REFS_MAP);
        Map::from(c)
    }

    /// Returns an [Array] data structure stored under a given `name`. Array structures are used for
    /// storing a sequences of elements in ordered manner, positioning given element accordingly
    /// to its index.
    ///
    /// If not structure under defined `name` existed before, it will be created and returned
    /// instead.
    ///
    /// If a structure under defined `name` already existed, but its type was different it will be
    /// reinterpreted as an array (in such case a sequence component of complex data type will be
    /// interpreted as a list of inserted values).
    pub fn get_array(&mut self, name: &str) -> Array {
        let c = self.store_mut().create_type(name, None, TYPE_REFS_ARRAY);
        Array::from(c)
    }

    /// Returns a [XmlElement] data structure stored under a given `name`. XML elements represent
    /// nodes of XML document. They can contain attributes (key-value pairs, both of string type)
    /// as well as other nested XML elements or text values, which are stored in their insertion
    /// order.
    ///
    /// If not structure under defined `name` existed before, it will be created and returned
    /// instead.
    ///
    /// If a structure under defined `name` already existed, but its type was different it will be
    /// reinterpreted as a XML element (in such case a map component of complex data type will be
    /// interpreted as map of its attributes, while a sequence component - as a list of its child
    /// XML nodes).
    pub fn get_xml_element(&mut self, name: &str) -> XmlElement {
        let c = self.store_mut().create_type(
            name,
            Some("UNDEFINED".to_string()),
            TYPE_REFS_XML_ELEMENT,
        );
        XmlElement::from(c)
    }

    /// Returns a [XmlText] data structure stored under a given `name`. Text structures are used for
    /// collaborative text editing: they expose operations to append and remove chunks of text,
    /// which are free to execute concurrently by multiple peers over remote boundaries.
    ///
    /// If not structure under defined `name` existed before, it will be created and returned
    /// instead.
    ///
    /// If a structure under defined `name` already existed, but its type was different it will be
    /// reinterpreted as a text (in such case a sequence component of complex data type will be
    /// interpreted as a list of text chunks).
    pub fn get_xml_text(&mut self, name: &str) -> XmlText {
        let c = self.store_mut().create_type(name, None, TYPE_REFS_XML_TEXT);
        XmlText::from(c)
    }

    /// Encodes the document state to a binary format.
    ///
    /// Document updates are idempotent and commutative. Caveats:
    /// * It doesn't matter in which order document updates are applied.
    /// * As long as all clients receive the same document updates, all clients
    ///   end up with the same content.
    /// * Even if an update contains known information, the unknown information
    ///   is extracted and integrated into the document structure.
    pub fn encode_update_v1(&self) -> Vec<u8> {
        let mut enc = updates::encoder::EncoderV1::new();
        let store = self.store();
        store.write_blocks(&self.before_state, &mut enc);
        self.delete_set.encode(&mut enc);
        enc.to_vec()
    }

    /// Applies given `id_set` onto current transaction to run multi-range deletion.
    /// Returns a remaining of original ID set, that couldn't be applied.
    pub(crate) fn apply_delete(&mut self, ds: &DeleteSet) -> Option<DeleteSet> {
        let mut unapplied = DeleteSet::new();
        for (client, ranges) in ds.iter() {
            let mut blocks = self.store_mut().blocks.get_mut(client).unwrap();
            let state = blocks.get_state();

            for range in ranges.iter() {
                let clock = range.start;
                let clock_end = range.end;

                if clock < state {
                    if state < clock_end {
                        unapplied.insert(ID::new(*client, clock), clock_end - state);
                    }
                    // We can ignore the case of GC and Delete structs, because we are going to skip them
                    if let Some(mut index) = blocks.find_pivot(clock) {
                        // We can ignore the case of GC and Delete structs, because we are going to skip them
                        if let Some(item) = blocks.get_mut(index).as_item_mut() {
                            // split the first item if necessary
                            if !item.is_deleted() && item.id.clock < clock {
                                let split_ptr =
                                    BlockPtr::new(ID::new(*client, clock), index as u32);
                                let (_, right) = self.store_mut().blocks.split_block(&split_ptr);
                                if let Some(right) = right {
                                    index += 1;
                                    self.merge_blocks.push(right.id);
                                }
                                blocks = self.store_mut().blocks.get_mut(client).unwrap();
                            }

                            while index < blocks.len() {
                                let block = blocks.get_mut(index);
                                if let Some(item) = block.as_item_mut() {
                                    if item.id.clock < clock_end {
                                        if !item.is_deleted() {
                                            let delete_ptr = BlockPtr::new(
                                                ID::new(*client, item.id.clock),
                                                index as u32,
                                            );
                                            if item.id.clock + item.len() > clock_end {
                                                let diff = clock_end - item.id.clock;
                                                let mut split_ptr = delete_ptr.clone();
                                                split_ptr.id.clock += diff;
                                                let (_, right) =
                                                    self.store_mut().blocks.split_block(&split_ptr);
                                                if let Some(right) = right {
                                                    self.merge_blocks.push(right.id);
                                                    index += 1;
                                                }
                                            }
                                            self.delete(&delete_ptr);
                                            blocks =
                                                self.store_mut().blocks.get_mut(client).unwrap();
                                            // just to make the borrow checker happy
                                        }
                                    } else {
                                        break;
                                    }
                                }
                                index += 1;
                            }
                        }
                    }
                } else {
                    unapplied.insert(ID::new(*client, clock), clock_end - clock);
                }
            }
        }

        if unapplied.is_empty() {
            None
        } else {
            Some(unapplied)
        }
    }

    /// Delete item under given pointer.
    /// Returns true if block was successfully deleted, false if it was already deleted in the past.
    pub(crate) fn delete(&mut self, ptr: &BlockPtr) -> bool {
        let mut recurse = Vec::new();
        let mut result = false;

        let store = unsafe { &mut *self.store.get() };
        if let Some(item) = store.blocks.get_item_mut(&ptr) {
            if !item.is_deleted() {
                if item.parent_sub.is_none() && item.is_countable() {
                    if let Some(parent) = self.store().get_type(&item.parent) {
                        let mut inner = parent.borrow_mut();
                        inner.block_len -= item.len();
                        inner.content_len -= item.content_len(store.options.offset_kind);
                    }
                }

                item.mark_as_deleted();
                self.delete_set.insert(item.id.clone(), item.len());

                match &item.parent {
                    TypePtr::Named(_) => {
                        self.changed
                            .entry(item.parent.clone())
                            .or_default()
                            .insert(item.parent_sub.clone());
                    }
                    TypePtr::Id(ptr)
                        if ptr.id.clock < self.before_state.get(&ptr.id.client)
                            && self.store().blocks.get_item(ptr).unwrap().is_deleted() =>
                    {
                        self.changed
                            .entry(item.parent.clone())
                            .or_default()
                            .insert(item.parent_sub.clone());
                    }
                    _ => {}
                }
                if item.id.clock < self.before_state.get(&item.id.client) {
                    let set = self.changed.entry(item.parent.clone()).or_default();
                    set.insert(item.parent_sub.clone());
                }

                match &item.content {
                    ItemContent::Doc(_, _) => {
                        //if (transaction.subdocsAdded.has(this.doc)) {
                        //    transaction.subdocsAdded.delete(this.doc)
                        //} else {
                        //    transaction.subdocsRemoved.add(this.doc)
                        //}
                        todo!()
                    }
                    ItemContent::Type(t) => {
                        let inner = t.borrow_mut();
                        let mut ptr = inner.start;
                        //TODO: self.changed.remove(&item.parent); // uncomment when deep observe is complete

                        while let Some(item) =
                            ptr.and_then(|ptr| self.store().blocks.get_item(&ptr))
                        {
                            if !item.is_deleted() {
                                recurse.push(ptr.unwrap());
                            }

                            ptr = item.right.clone();
                        }

                        for ptr in inner.map.values() {
                            recurse.push(ptr.clone());
                        }
                    }
                    _ => { /* nothing to do for other content types */ }
                }
                result = true;
            }
        }

        for ptr in recurse.iter() {
            if !self.delete(ptr) {
                // Whis will be gc'd later and we want to merge it if possible
                // We try to merge all deleted items after each transaction,
                // but we have no knowledge about that this needs to be merged
                // since it is not in transaction.ds. Hence we add it to transaction._mergeStructs
                self.merge_blocks.push(ptr.id);
            }
        }

        result
    }

    pub fn apply_update(&mut self, mut update: Update) {
        if self.store().update_events.has_subscribers() {
            let event = UpdateEvent::new(update);
            self.store().update_events.publish(self, &event);
            update = event.update;
        }
        let (remaining, remaining_ds) = update.integrate(self);
        let mut retry = false;
        {
            let store = self.store_mut();
            if let Some(mut pending) = store.pending.take() {
                // check if we can apply something
                for (client, &clock) in pending.missing.iter() {
                    if clock < store.blocks.get_state(client) {
                        retry = true;
                        break;
                    }
                }

                if let Some(remaining) = remaining {
                    // merge restStructs into store.pending
                    for (&client, &clock) in remaining.missing.iter() {
                        pending.missing.set_min(client, clock);
                    }
                    pending.update = Update::merge_updates(vec![pending.update, remaining.update]);
                    store.pending = Some(pending);
                }
            } else {
                store.pending = remaining;
            }
        }
        if let Some(pending) = self.store_mut().pending_ds.take() {
            let ds2 = self.apply_delete(&pending);
            let ds = match (remaining_ds, ds2) {
                (Some(mut a), Some(b)) => {
                    a.delete_set.merge(b);
                    Some(a.delete_set)
                }
                (Some(x), _) => Some(x.delete_set),
                (_, Some(x)) => Some(x),
                _ => None,
            };
            self.store_mut().pending_ds = ds;
        } else {
            self.store_mut().pending_ds = remaining_ds.map(|update| update.delete_set);
        }

        if retry {
            let store = self.store_mut();
            if let Some(pending) = store.pending.take() {
                let ds = store.pending_ds.take().unwrap_or_default();
                let mut ds_update = Update::new();
                ds_update.delete_set = ds;
                self.apply_update(pending.update);
                self.apply_update(ds_update)
            }
        }
    }

    pub(crate) fn create_item<T: Prelim>(
        &mut self,
        pos: &block::ItemPosition,
        value: T,
        parent_sub: Option<Rc<str>>,
    ) -> &Item {
        let (left, right, origin, ptr) = {
            let store = self.store_mut();
            let left = pos.left;
            let right = pos.right;
            let origin = if let Some(ptr) = pos.left.as_ref() {
                if let Some(item) = store.blocks.get_item(ptr) {
                    Some(item.last_id())
                } else {
                    None
                }
            } else {
                None
            };
            let client_id = store.options.client_id;
            let id = block::ID {
                client: client_id,
                clock: store.get_local_state(),
            };
            let pivot = store
                .blocks
                .get_client_blocks_mut(client_id)
                .integrated_len() as u32;

            let ptr = BlockPtr::new(id, pivot);
            (left, right, origin, ptr)
        };
        let (content, remainder) = value.into_content(self, TypePtr::Id(ptr.clone()));
        let inner_ref = if let ItemContent::Type(inner_ref) = &content {
            Some(inner_ref.clone())
        } else {
            None
        };
        let mut item = Item::new(
            ptr.id,
            left,
            origin,
            right,
            right.map(|r| r.id),
            pos.parent.clone(),
            parent_sub,
            content,
        );

        item.integrate(self, ptr.pivot() as u32, 0);

        let local_block_list = self.store_mut().blocks.get_client_blocks_mut(ptr.id.client);
        local_block_list.push(block::Block::Item(item));

        let idx = local_block_list.len() - 1;

        if let Some(remainder) = remainder {
            remainder.integrate(self, inner_ref.unwrap())
        }

        self.store_mut().blocks.get_client_blocks_mut(ptr.id.client)[idx]
            .as_item()
            .unwrap()
    }

    /// Commits current transaction. This step involves cleaning up and optimizing changes performed
    /// during lifetime of a transaction. Such changes include squashing delete sets data
    /// or squashing blocks that have been appended one after another to preserve memory.
    ///
    /// This step is performed automatically when a transaction is about to be dropped (its life
    /// scope comes to an end).
    pub fn commit(&mut self) {
        if self.committed {
            return;
        }
        self.committed = true;

        // 1. sort and merge delete set
        let store = unsafe { &mut *self.store.get() };
        self.delete_set.squash();
        self.after_state = store.blocks.get_state_vector();
        // 2. emit 'beforeObserverCalls'
        // 3. for each change observed by the transaction call 'afterTransaction'
        if !self.changed.is_empty() {
            for (ptr, subs) in self.changed.iter() {
                if let Some(branch) = store.get_type(ptr) {
                    branch.trigger(self, subs.clone());
                }
            }
        }

        // 4. try GC delete set
        if !store.options.skip_gc {
            self.try_gc();
        }

        // 5. try merge delete set
        self.delete_set.try_squash_with(store);

        // 6. get transaction after state and try to merge to left
        for (client, &clock) in self.after_state.iter() {
            let before_clock = self.before_state.get(client);
            if before_clock != clock {
                let mut blocks = store.blocks.get_mut(client).unwrap();
                let first_change = blocks.find_pivot(before_clock).unwrap().max(1);
                let mut i = blocks.len() - 1;
                while i >= first_change {
                    if let Some(compaction) = blocks.squash_left(i) {
                        store.gc_cleanup(compaction);
                        blocks = store.blocks.get_mut(client).unwrap();
                    }
                    i -= 1;
                }
            }
        }
        // 7. get merge_structs and try to merge to left
        for id in self.merge_blocks.iter() {
            let client = id.client;
            let clock = id.clock;
            let blocks = store.blocks.get_mut(&client).unwrap();
            let replaced_pos = blocks.find_pivot(clock).unwrap();
            if replaced_pos + 1 < blocks.len() {
                if let Some(compaction) = blocks.squash_left(replaced_pos + 1) {
                    store.gc_cleanup(compaction);
                }
            } else if replaced_pos > 0 {
                if let Some(compaction) = blocks.squash_left(replaced_pos) {
                    store.gc_cleanup(compaction);
                }
            }
        }
        // 8. emit 'afterTransactionCleanup'
        // 9. emit 'update'
        // 10. emit 'updateV2'
        // 11. add and remove subdocs
        // 12. emit 'subdocs'
    }

    fn try_gc(&self) {
        let store = self.store();
        for (client, range) in self.delete_set.iter() {
            if let Some(blocks) = store.blocks.get(client) {
                for delete_item in range.iter().rev() {
                    let mut start = delete_item.start;
                    if let Some(mut i) = blocks.find_pivot(start) {
                        while i < blocks.len() {
                            let block = blocks.get_mut(i);
                            let len = block.len();
                            start += len;
                            if start > delete_item.end {
                                break;
                            } else {
                                block.gc(self, false);
                                i += 1;
                            }
                        }
                    }
                }
            }
        }
    }

    pub(crate) fn add_changed_type(&mut self, parent: &Branch, parent_sub: Option<Rc<str>>) {
        let trigger = match &parent.ptr {
            TypePtr::Named(_) => true,
            TypePtr::Id(ptr) if ptr.id.clock < (self.before_state.get(&ptr.id.client)) => {
                if let Some(item) = self.store().blocks.get_item(ptr) {
                    !item.is_deleted()
                } else {
                    false
                }
            }
            _ => false,
        };
        if trigger {
            let e = self.changed.entry(parent.ptr.clone()).or_default();
            e.insert(parent_sub.clone());
        }
    }

    /// Checks if item with a given `id` has been added to a block store within this transaction.
    pub(crate) fn has_added(&self, id: &ID) -> bool {
        id.clock >= self.before_state.get(&id.client)
    }

    /// Checks if item with a given `id` has been deleted within this transaction.
    pub(crate) fn has_deleted(&self, id: &ID) -> bool {
        self.delete_set.is_deleted(id)
    }

    pub(crate) fn split_by_snapshot(&mut self, snapshot: &Snapshot) {
        let blocks = &mut self.store_mut().blocks;
        for (client, &clock) in snapshot.state_map.iter() {
            if let Some(list) = blocks.get(client) {
                if clock < list.get_state() {
                    let ptr = BlockPtr::new(ID::new(*client, clock), (list.len() - 1) as u32);
                    blocks.split_block(&ptr);
                }
            }
        }

        for (client, range) in snapshot.delete_set.iter() {
            if let Some(mut list) = blocks.get(client) {
                for r in range.iter() {
                    if let Some(pivot) = list.find_pivot(r.start) {
                        let block = &list[pivot];
                        if block.id().clock < r.start {
                            blocks.split_block(&BlockPtr::new(
                                ID::new(*client, r.start),
                                pivot as u32,
                            ));
                            list = blocks.get(client).unwrap();
                        }
                    }

                    if let Some(pivot) = list.find_pivot(r.end) {
                        let block = &list[pivot];
                        if block.id().clock + block.len() > r.end {
                            blocks
                                .split_block(&BlockPtr::new(ID::new(*client, r.end), pivot as u32));
                            list = blocks.get(client).unwrap();
                        }
                    }
                }
            }
        }
    }
}

impl Drop for Transaction {
    fn drop(&mut self) {
        self.commit()
    }
}
