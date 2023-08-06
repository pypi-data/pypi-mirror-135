use crate::block::{ItemContent, ItemPosition, Prelim};
use crate::event::Subscription;
use crate::types::{
    event_keys, Branch, BranchRef, Entries, EntryChange, Observers, Path, TypePtr, Value,
    TYPE_REFS_MAP,
};
use crate::*;
use lib0::any::Any;
use std::cell::UnsafeCell;
use std::collections::{HashMap, HashSet};
use std::rc::Rc;

/// Collection used to store key-value entries in an unordered manner. Keys are always represented
/// as UTF-8 strings. Values can be any value type supported by Yrs: JSON-like primitives as well as
/// shared data types.
///
/// In terms of conflict resolution, [Map] uses logical last-write-wins principle, meaning the past
/// updates are automatically overridden and discarded by newer ones, while concurrent updates made
/// by different peers are resolved into a single value using document id seniority to establish
/// order.
#[derive(Debug, Clone, Eq, PartialEq)]
pub struct Map(BranchRef);

impl Map {
    /// Converts all entries of a current map into JSON-like object representation.
    pub fn to_json(&self, txn: &Transaction) -> Any {
        let inner = self.0.as_ref();
        let mut res = HashMap::new();
        for (key, ptr) in inner.map.iter() {
            if let Some(item) = txn.store().blocks.get_item(ptr) {
                if !item.is_deleted() {
                    let any = if let Some(value) = item.content.get_content_last(txn) {
                        value.to_json(txn)
                    } else {
                        Any::Null
                    };
                    res.insert(key.to_string(), any);
                }
            }
        }
        Any::Map(Box::new(res))
    }

    /// Returns a number of entries stored within current map.
    pub fn len(&self, txn: &Transaction) -> u32 {
        let mut len = 0;
        let inner = self.0.borrow();
        for ptr in inner.map.values() {
            //TODO: maybe it would be better to just cache len in the map itself?
            if let Some(item) = txn.store().blocks.get_item(ptr) {
                if !item.is_deleted() {
                    len += 1;
                }
            }
        }
        len
    }

    fn entries<'a, 'b>(&'a self, txn: &'b Transaction) -> Entries<'b> {
        let ptr = &self.0.borrow().ptr;
        Entries::new(ptr, txn)
    }

    /// Returns an iterator that enables to traverse over all keys of entries stored within
    /// current map. These keys are not ordered.
    pub fn keys<'a, 'b>(&'a self, txn: &'b Transaction) -> Keys<'b> {
        Keys(self.entries(txn))
    }

    /// Returns an iterator that enables to traverse over all values stored within current map.
    pub fn values<'a, 'b>(&'a self, txn: &'b Transaction) -> Values<'b> {
        Values(self.entries(txn))
    }

    /// Returns an iterator that enables to traverse over all entries - tuple of key-value pairs -
    /// stored within current map.
    pub fn iter<'a, 'b>(&'a self, txn: &'b Transaction) -> MapIter<'b> {
        MapIter(self.entries(txn))
    }

    /// Inserts a new `value` under given `key` into current map. Returns a value stored previously
    /// under the same key (if any existed).
    pub fn insert<K: Into<Rc<str>>, V: Prelim>(
        &self,
        txn: &mut Transaction,
        key: K,
        value: V,
    ) -> Option<Value> {
        let key = key.into();
        let previous = self.get(txn, &key);
        let pos = {
            let inner = self.0.borrow();
            let left = inner.map.get(&key);
            ItemPosition {
                parent: inner.ptr.clone(),
                left: left.cloned(),
                right: None,
                index: 0,
                current_attrs: None,
            }
        };

        txn.create_item(&pos, value, Some(key));
        previous
    }

    /// Removes a stored within current map under a given `key`. Returns that value or `None` if
    /// no entry with a given `key` was present in current map.
    pub fn remove(&self, txn: &mut Transaction, key: &str) -> Option<Value> {
        let t = self.0.borrow();
        t.remove(txn, key)
    }

    /// Returns a value stored under a given `key` within current map, or `None` if no entry
    /// with such `key` existed.
    pub fn get(&self, txn: &Transaction, key: &str) -> Option<Value> {
        let t = self.0.borrow();
        t.get(txn, key)
    }

    /// Checks if an entry with given `key` can be found within current map.
    pub fn contains(&self, txn: &Transaction, key: &str) -> bool {
        let t = self.0.borrow();
        if let Some(ptr) = t.map.get(key) {
            if let Some(item) = txn.store().blocks.get_item(ptr) {
                return !item.is_deleted();
            }
        }
        false
    }

    /// Clears the contents of current map, effectively removing all of its entries.
    pub fn clear(&self, txn: &mut Transaction) {
        let t = self.0.borrow();
        for (_, ptr) in t.map.iter() {
            txn.delete(ptr);
        }
    }

    /// Subscribes a given callback to be triggered whenever current map is changed.
    /// A callback is triggered whenever a transaction gets committed. This function does not
    /// trigger if changes have been observed by nested shared collections.
    ///
    /// All map changes can be tracked by using [Event::keys] method.
    ///
    /// Returns an [Observer] which, when dropped, will unsubscribe current callback.
    pub fn observe<F>(&self, f: F) -> Subscription<MapEvent>
    where
        F: Fn(&Transaction, &MapEvent) -> () + 'static,
    {
        let mut branch = self.0.borrow_mut();
        if let Observers::Map(eh) = branch.observers.get_or_insert_with(Observers::map) {
            eh.subscribe(f)
        } else {
            panic!("Observed collection is of different type") //TODO: this should be Result::Err
        }
    }

    /// Unsubscribes a previously subscribed event callback identified by given `subscription_id`.
    pub fn unobserve(&self, subscription_id: SubscriptionId) {
        let mut branch = self.0.borrow_mut();
        if let Some(Observers::Map(eh)) = branch.observers.as_mut() {
            eh.unsubscribe(subscription_id);
        }
    }
}

pub struct MapIter<'a>(Entries<'a>);

impl<'a> Iterator for MapIter<'a> {
    type Item = (&'a str, Value);

    fn next(&mut self) -> Option<Self::Item> {
        let (key, item) = self.0.next()?;
        if let Some(content) = item.content.get_content_last(self.0.txn) {
            Some((key, content))
        } else {
            self.next()
        }
    }
}

/// An unordered iterator over the keys of a [Map].
pub struct Keys<'a>(Entries<'a>);

impl<'a> Iterator for Keys<'a> {
    type Item = &'a str;

    fn next(&mut self) -> Option<Self::Item> {
        let (key, _) = self.0.next()?;
        Some(key)
    }
}

/// Iterator over the values of a [Map].
pub struct Values<'a>(Entries<'a>);

impl<'a> Iterator for Values<'a> {
    type Item = Vec<Value>;

    fn next(&mut self) -> Option<Self::Item> {
        let (_, item) = self.0.next()?;
        Some(item.content.get_content(self.0.txn))
    }
}

impl From<BranchRef> for Map {
    fn from(inner: BranchRef) -> Self {
        Map(inner)
    }
}

/// A preliminary map. It can be used to early initialize the contents of a [Map], when it's about
/// to be inserted into another Yrs collection, such as [Array] or another [Map].
pub struct PrelimMap<T>(HashMap<String, T>);

impl<T> From<HashMap<String, T>> for PrelimMap<T> {
    fn from(map: HashMap<String, T>) -> Self {
        PrelimMap(map)
    }
}

impl<T: Prelim> Prelim for PrelimMap<T> {
    fn into_content(self, _txn: &mut Transaction, ptr: TypePtr) -> (ItemContent, Option<Self>) {
        let inner = BranchRef::new(Branch::new(ptr, TYPE_REFS_MAP, None));
        (ItemContent::Type(inner), Some(self))
    }

    fn integrate(self, txn: &mut Transaction, inner_ref: BranchRef) {
        let map = Map::from(inner_ref);
        for (key, value) in self.0 {
            map.insert(txn, key, value);
        }
    }
}

/// Event generated by [Map::observe] method. Emitted during transaction commit phase.
pub struct MapEvent {
    target: Map,
    current_target: BranchRef,
    keys: UnsafeCell<Result<HashMap<Rc<str>, EntryChange>, HashSet<Option<Rc<str>>>>>,
}

impl MapEvent {
    pub(crate) fn new(branch_ref: BranchRef, key_changes: HashSet<Option<Rc<str>>>) -> Self {
        let current_target = branch_ref.clone();
        MapEvent {
            target: Map::from(branch_ref),
            current_target,
            keys: UnsafeCell::new(Err(key_changes)),
        }
    }

    /// Returns a [Map] instance which emitted this event.
    pub fn target(&self) -> &Map {
        &self.target
    }

    /// Returns a path from root type down to [Map] instance which emitted this event.
    pub fn path(&self, txn: &Transaction) -> Path {
        Branch::path(self.current_target.borrow(), self.target.0.borrow(), txn)
    }

    /// Returns a summary of key-value changes made over corresponding [Map] collection within
    /// bounds of current transaction.
    pub fn keys(&self, txn: &Transaction) -> &HashMap<Rc<str>, EntryChange> {
        let keys = unsafe { self.keys.get().as_mut().unwrap() };

        match keys {
            Ok(keys) => {
                return keys;
            }
            Err(subs) => {
                let subs = event_keys(txn, self.target.0.borrow(), subs);
                *keys = Ok(subs);
                if let Ok(keys) = keys {
                    keys
                } else {
                    panic!("Defect: should not happen");
                }
            }
        }
    }
}

#[cfg(test)]
mod test {
    use crate::test_utils::{exchange_updates, run_scenario};
    use crate::types::{EntryChange, Map, Value};
    use crate::updates::decoder::Decode;
    use crate::updates::encoder::{Encoder, EncoderV1};
    use crate::{Doc, PrelimArray, PrelimMap, Transaction, Update};
    use lib0::any::Any;
    use rand::distributions::Alphanumeric;
    use rand::prelude::{SliceRandom, StdRng};
    use rand::Rng;
    use std::cell::RefCell;
    use std::collections::HashMap;
    use std::rc::Rc;

    #[test]
    fn map_basic() {
        let d1 = Doc::with_client_id(1);
        let mut t1 = d1.transact();
        let m1 = t1.get_map("map");

        let d2 = Doc::with_client_id(2);
        let mut t2 = d2.transact();
        let m2 = t2.get_map("map");

        m1.insert(&mut t1, "number".to_owned(), 1);
        m1.insert(&mut t1, "string".to_owned(), "hello Y");
        m1.insert(&mut t1, "object".to_owned(), {
            let mut v = HashMap::new();
            v.insert("key2".to_owned(), "value");

            let mut map = HashMap::new();
            map.insert("key".to_owned(), v);
            map // { key: { key2: 'value' } }
        });
        m1.insert(&mut t1, "boolean1".to_owned(), true);
        m1.insert(&mut t1, "boolean0".to_owned(), false);

        //let m1m = t1.get_map("y-map");
        //let m1a = t1.get_text("y-text");
        //m1a.insert(&mut t1, 0, "a");
        //m1a.insert(&mut t1, 0, "b");
        //m1m.insert(&mut t1, "y-text".to_owned(), m1a);

        //TODO: YArray within YMap
        fn compare_all(t: &Transaction, m: &Map) {
            assert_eq!(m.len(&t), 5);
            assert_eq!(m.get(&t, &"number".to_owned()), Some(Value::from(1f64)));
            assert_eq!(m.get(&t, &"boolean0".to_owned()), Some(Value::from(false)));
            assert_eq!(m.get(&t, &"boolean1".to_owned()), Some(Value::from(true)));
            assert_eq!(
                m.get(&t, &"string".to_owned()),
                Some(Value::from("hello Y"))
            );
            assert_eq!(
                m.get(&t, &"object".to_owned()),
                Some(Value::from({
                    let mut m = HashMap::new();
                    let mut n = HashMap::new();
                    n.insert("key2".to_owned(), Any::String("value".into()));
                    m.insert("key".to_owned(), Any::Map(Box::new(n)));
                    m
                }))
            );
        }

        compare_all(&t1, &m1);

        let update = d1.encode_state_as_update_v1(&t1);
        d2.apply_update_v1(&mut t2, update.as_slice());

        compare_all(&t2, &m2);
    }

    #[test]
    fn map_get_set() {
        let d1 = Doc::with_client_id(1);
        let mut t1 = d1.transact();
        let m1 = t1.get_map("map");

        m1.insert(&mut t1, "stuff".to_owned(), "stuffy");
        m1.insert(&mut t1, "null".to_owned(), None as Option<String>);

        let update = d1.encode_state_as_update_v1(&t1);

        let d2 = Doc::with_client_id(2);
        let mut t2 = d2.transact();

        d2.apply_update_v1(&mut t2, update.as_slice());

        let m2 = t2.get_map("map");
        assert_eq!(
            m2.get(&t2, &"stuff".to_owned()),
            Some(Value::from("stuffy"))
        );
        assert_eq!(m2.get(&t2, &"null".to_owned()), Some(Value::Any(Any::Null)));
    }

    #[test]
    fn map_get_set_sync_with_conflicts() {
        let d1 = Doc::with_client_id(1);
        let mut t1 = d1.transact();
        let m1 = t1.get_map("map");

        let d2 = Doc::with_client_id(2);
        let mut t2 = d2.transact();
        let m2 = t2.get_map("map");

        m1.insert(&mut t1, "stuff".to_owned(), "c0");
        m2.insert(&mut t2, "stuff".to_owned(), "c1");

        let u1 = d1.encode_state_as_update_v1(&t1);
        let u2 = d2.encode_state_as_update_v1(&t2);

        d1.apply_update_v1(&mut t1, u2.as_slice());
        d2.apply_update_v1(&mut t2, u1.as_slice());

        assert_eq!(m1.get(&t1, &"stuff".to_owned()), Some(Value::from("c1")));
        assert_eq!(m2.get(&t2, &"stuff".to_owned()), Some(Value::from("c1")));
    }

    #[test]
    fn map_len_remove() {
        let d1 = Doc::with_client_id(1);
        let mut t1 = d1.transact();
        let m1 = t1.get_map("map");

        let key1 = "stuff".to_owned();
        let key2 = "other-stuff".to_owned();

        m1.insert(&mut t1, key1.clone(), "c0");
        m1.insert(&mut t1, key2.clone(), "c1");
        assert_eq!(m1.len(&t1), 2);

        // remove 'stuff'
        assert_eq!(m1.remove(&mut t1, &key1), Some(Value::from("c0")));
        assert_eq!(m1.len(&t1), 1);

        // remove 'stuff' again - nothing should happen
        assert_eq!(m1.remove(&mut t1, &key1), None);
        assert_eq!(m1.len(&t1), 1);

        // remove 'other-stuff'
        assert_eq!(m1.remove(&mut t1, &key2), Some(Value::from("c1")));
        assert_eq!(m1.len(&t1), 0);
    }

    #[test]
    fn map_clear() {
        let d1 = Doc::with_client_id(1);
        let mut t1 = d1.transact();
        let m1 = t1.get_map("map");

        m1.insert(&mut t1, "key1".to_owned(), "c0");
        m1.insert(&mut t1, "key2".to_owned(), "c1");
        m1.clear(&mut t1);

        assert_eq!(m1.len(&t1), 0);
        assert_eq!(m1.get(&t1, &"key1".to_owned()), None);
        assert_eq!(m1.get(&t1, &"key2".to_owned()), None);

        let d2 = Doc::with_client_id(2);
        let mut t2 = d2.transact();

        let u1 = d1.encode_state_as_update_v1(&t1);
        d2.apply_update_v1(&mut t2, u1.as_slice());

        let m2 = t2.get_map("map");
        assert_eq!(m2.len(&t2), 0);
        assert_eq!(m2.get(&t2, &"key1".to_owned()), None);
        assert_eq!(m2.get(&t2, &"key2".to_owned()), None);
    }

    #[test]
    fn map_clear_sync() {
        let d1 = Doc::with_client_id(1);
        let d2 = Doc::with_client_id(2);
        let d3 = Doc::with_client_id(3);
        let d4 = Doc::with_client_id(4);

        {
            let mut t1 = d1.transact();
            let mut t2 = d2.transact();
            let mut t3 = d3.transact();

            let m1 = t1.get_map("map");
            let m2 = t2.get_map("map");
            let m3 = t3.get_map("map");

            m1.insert(&mut t1, "key1".to_owned(), "c0");
            m2.insert(&mut t2, "key1".to_owned(), "c1");
            m2.insert(&mut t2, "key1".to_owned(), "c2");
            m3.insert(&mut t3, "key1".to_owned(), "c3");
        }

        exchange_updates(&[&d1, &d2, &d3, &d4]);

        {
            let mut t1 = d1.transact();
            let mut t2 = d2.transact();
            let mut t3 = d3.transact();

            let m1 = t1.get_map("map");
            let m2 = t2.get_map("map");
            let m3 = t3.get_map("map");

            m1.insert(&mut t1, "key2".to_owned(), "c0");
            m2.insert(&mut t2, "key2".to_owned(), "c1");
            m2.insert(&mut t2, "key2".to_owned(), "c2");
            m3.insert(&mut t3, "key2".to_owned(), "c3");
            m3.clear(&mut t3);
        }

        exchange_updates(&[&d1, &d2, &d3, &d4]);

        for doc in [d1, d2, d3, d4] {
            let mut txn = doc.transact();
            let map = txn.get_map("map");

            assert_eq!(
                map.get(&txn, &"key1".to_owned()),
                None,
                "'key1' entry for peer {} should be removed",
                doc.client_id
            );
            assert_eq!(
                map.get(&txn, &"key2".to_owned()),
                None,
                "'key2' entry for peer {} should be removed",
                doc.client_id
            );
            assert_eq!(
                map.len(&txn),
                0,
                "all entries for peer {} should be removed",
                doc.client_id
            );
        }
    }

    #[test]
    fn map_get_set_with_3_way_conflicts() {
        let d1 = Doc::with_client_id(1);
        let d2 = Doc::with_client_id(2);
        let d3 = Doc::with_client_id(3);

        {
            let mut t1 = d1.transact();
            let mut t2 = d2.transact();
            let mut t3 = d3.transact();

            let m1 = t1.get_map("map");
            let m2 = t2.get_map("map");
            let m3 = t3.get_map("map");

            m1.insert(&mut t1, "stuff".to_owned(), "c0");
            m2.insert(&mut t2, "stuff".to_owned(), "c1");
            m2.insert(&mut t2, "stuff".to_owned(), "c2");
            m3.insert(&mut t3, "stuff".to_owned(), "c3");
        }

        exchange_updates(&[&d1, &d2, &d3]);

        for doc in [d1, d2, d3] {
            let mut txn = doc.transact();

            let map = txn.get_map("map");

            assert_eq!(
                map.get(&txn, &"stuff".to_owned()),
                Some(Value::from("c3")),
                "peer {} - map entry resolved to unexpected value",
                doc.client_id
            );
        }
    }

    #[test]
    fn map_get_set_remove_with_3_way_conflicts() {
        let d1 = Doc::with_client_id(1);
        let d2 = Doc::with_client_id(2);
        let d3 = Doc::with_client_id(3);
        let d4 = Doc::with_client_id(4);

        {
            let mut t1 = d1.transact();
            let mut t2 = d2.transact();
            let mut t3 = d3.transact();

            let m1 = t1.get_map("map");
            let m2 = t2.get_map("map");
            let m3 = t3.get_map("map");

            m1.insert(&mut t1, "key1".to_owned(), "c0");
            m2.insert(&mut t2, "key1".to_owned(), "c1");
            m2.insert(&mut t2, "key1".to_owned(), "c2");
            m3.insert(&mut t3, "key1".to_owned(), "c3");
        }

        exchange_updates(&[&d1, &d2, &d3, &d4]);

        {
            let mut t1 = d1.transact();
            let mut t2 = d2.transact();
            let mut t3 = d3.transact();
            let mut t4 = d4.transact();

            let m1 = t1.get_map("map");
            let m2 = t2.get_map("map");
            let m3 = t3.get_map("map");
            let m4 = t4.get_map("map");

            m1.insert(&mut t1, "key1".to_owned(), "deleteme");
            m2.insert(&mut t2, "key1".to_owned(), "c1");
            m3.insert(&mut t3, "key1".to_owned(), "c2");
            m4.insert(&mut t4, "key1".to_owned(), "c3");
            m4.remove(&mut t4, &"key1".to_owned());
        }

        exchange_updates(&[&d1, &d2, &d3, &d4]);

        for doc in [d1, d2, d3, d4] {
            let mut txn = doc.transact();
            let map = txn.get_map("map");

            assert_eq!(
                map.get(&txn, &"key1".to_owned()),
                None,
                "entry 'key1' on peer {} should be removed",
                doc.client_id
            );
        }
    }

    #[test]
    fn insert_and_remove_events() {
        let d1 = Doc::with_client_id(1);
        let m1 = {
            let mut txn = d1.transact();
            txn.get_map("map")
        };

        let entries = Rc::new(RefCell::new(None));
        let entries_c = entries.clone();
        let _sub = m1.observe(move |txn, e| {
            let keys = e.keys(txn);
            *entries_c.borrow_mut() = Some(keys.clone());
        });

        // insert new entry
        {
            let mut txn = d1.transact();
            m1.insert(&mut txn, "a", 1);
            // txn is committed at the end of this scope
        }
        assert_eq!(
            entries.take(),
            Some(HashMap::from([(
                "a".into(),
                EntryChange::Inserted(Any::Number(1.0).into())
            )]))
        );

        // update existing entry once
        {
            let mut txn = d1.transact();
            m1.insert(&mut txn, "a", 2);
        }
        assert_eq!(
            entries.take(),
            Some(HashMap::from([(
                "a".into(),
                EntryChange::Updated(Any::Number(1.0).into(), Any::Number(2.0).into())
            )]))
        );

        // update existing entry twice
        {
            let mut txn = d1.transact();
            m1.insert(&mut txn, "a", 3);
            m1.insert(&mut txn, "a", 4);
        }
        assert_eq!(
            entries.take(),
            Some(HashMap::from([(
                "a".into(),
                EntryChange::Updated(Any::Number(2.0).into(), Any::Number(4.0).into())
            )]))
        );

        // remove existing entry
        {
            let mut txn = d1.transact();
            m1.remove(&mut txn, "a");
        }
        assert_eq!(
            entries.take(),
            Some(HashMap::from([(
                "a".into(),
                EntryChange::Removed(Any::Number(4.0).into())
            )]))
        );

        // add another entry and update it
        {
            let mut txn = d1.transact();
            m1.insert(&mut txn, "b", 1);
            m1.insert(&mut txn, "b", 2);
        }
        assert_eq!(
            entries.take(),
            Some(HashMap::from([(
                "b".into(),
                EntryChange::Inserted(Any::Number(2.0).into())
            )]))
        );

        // add and remove an entry
        {
            let mut txn = d1.transact();
            m1.insert(&mut txn, "c", 1);
            m1.remove(&mut txn, "c");
        }
        assert_eq!(entries.take(), Some(HashMap::new()));

        // copy updates over
        let d2 = Doc::with_client_id(2);
        let m2 = {
            let mut txn = d2.transact();
            txn.get_map("map")
        };

        let entries = Rc::new(RefCell::new(None));
        let entries_c = entries.clone();
        let _sub = m2.observe(move |txn, e| {
            let keys = e.keys(txn);
            *entries_c.borrow_mut() = Some(keys.clone());
        });

        {
            let t1 = d1.transact();
            let mut t2 = d2.transact();

            let sv = t2.state_vector();
            let mut encoder = EncoderV1::new();
            t1.encode_diff(&sv, &mut encoder);
            t2.apply_update(Update::decode_v1(encoder.to_vec().as_slice()));
        }
        assert_eq!(
            entries.take(),
            Some(HashMap::from([(
                "b".into(),
                EntryChange::Inserted(Any::Number(2.0).into())
            )]))
        );
    }

    fn random_string(rng: &mut StdRng) -> String {
        let len = rng.gen_range(1, 10);
        rng.sample_iter(&Alphanumeric)
            .take(len)
            .map(char::from)
            .collect()
    }

    fn map_transactions() -> [Box<dyn Fn(&mut Doc, &mut StdRng)>; 3] {
        fn set(doc: &mut Doc, rng: &mut StdRng) {
            let mut txn = doc.transact();
            let map = txn.get_map("map");
            let key = ["one", "two"].choose(rng).unwrap();
            let value: String = random_string(rng);
            map.insert(&mut txn, key.to_string(), value);
        }

        fn set_type(doc: &mut Doc, rng: &mut StdRng) {
            let mut txn = doc.transact();
            let map = txn.get_map("map");
            let key = ["one", "two"].choose(rng).unwrap();
            if rng.gen_bool(0.5) {
                map.insert(
                    &mut txn,
                    key.to_string(),
                    PrelimArray::from(vec![1, 2, 3, 4]),
                );
            } else {
                map.insert(
                    &mut txn,
                    key.to_string(),
                    PrelimMap::from({
                        let mut map = HashMap::default();
                        map.insert("deepkey".to_owned(), "deepvalue");
                        map
                    }),
                );
            }
        }

        fn delete(doc: &mut Doc, rng: &mut StdRng) {
            let mut txn = doc.transact();
            let map = txn.get_map("map");
            let key = ["one", "two"].choose(rng).unwrap();
            map.remove(&mut txn, key);
        }
        [Box::new(set), Box::new(set_type), Box::new(delete)]
    }

    fn fuzzy(iterations: usize) {
        run_scenario(0, &map_transactions(), 5, iterations)
    }

    #[test]
    fn fuzzy_test_6() {
        fuzzy(6)
    }
}
