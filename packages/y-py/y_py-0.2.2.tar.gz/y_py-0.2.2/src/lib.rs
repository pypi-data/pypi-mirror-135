use lib0::any::Any;
use pyo3::exceptions::PyIndexError;
use pyo3::prelude::*;
use pyo3::types as pytypes;
use pyo3::types::PyByteArray;
use pyo3::types::PyList;
use pyo3::types::PyTuple;
use pyo3::types::{PyAny, PyDict};
use pyo3::wrap_pyfunction;
use pyo3::PyIterProtocol;
use std::collections::HashMap;
use std::convert::TryFrom;
use std::mem::ManuallyDrop;
use std::ops::{Deref, DerefMut};
use yrs;
use yrs::block::{ItemContent, Prelim};
use yrs::types::array::ArrayIter;
use yrs::types::map::MapIter;
use yrs::types::xml::{Attributes, TreeWalker, XmlEvent, XmlTextEvent};
use yrs::types::Attrs;
use yrs::types::Change;
use yrs::types::Delta;
use yrs::types::EntryChange;
use yrs::types::Path;
use yrs::types::PathSegment;
use yrs::types::TYPE_REFS_XML_ELEMENT;
use yrs::types::TYPE_REFS_XML_TEXT;
use yrs::types::{
    Branch, BranchRef, TypePtr, TypeRefs, Value, TYPE_REFS_ARRAY, TYPE_REFS_MAP, TYPE_REFS_TEXT,
};
use yrs::updates::decoder::{Decode, DecoderV1};
use yrs::updates::encoder::{Encode, Encoder, EncoderV1};
use yrs::OffsetKind;
use yrs::Options;
use yrs::Subscription;
use yrs::Xml;
use yrs::XmlElement;
use yrs::XmlText;
use yrs::{Array, Doc, Map, StateVector, Text, Transaction, Update};

/// A y-py document type. Documents are most important units of collaborative resources management.
/// All shared collections live within a scope of their corresponding documents. All updates are
/// generated on per document basis (rather than individual shared type). All operations on shared
/// collections happen via [YTransaction], which lifetime is also bound to a document.
///
/// Document manages so called root types, which are top-level shared types definitions (as opposed
/// to recursively nested types).
///
/// A basic workflow sample:
///
/// ```python
/// from y_py import YDoc
///
/// doc = YDoc()
/// with doc.begin_transaction() as txn:
///     text = txn.get_text('name')
///     text.push(txn, 'hello world')
///     output = text.to_string(txn)
///     print(output)
/// ```
#[pyclass(unsendable)]
pub struct YDoc(Doc);

#[pymethods]
impl YDoc {
    /// Doc(id)
    /// --
    ///
    /// Creates a new y-py document. If `id` parameter was passed it will be used as this document
    /// globally unique identifier (it's up to caller to ensure that requirement). Otherwise it will
    /// be assigned a randomly generated number.
    #[new]
    pub fn new(
        client_id: Option<u64>,
        offset_kind: Option<String>,
        skip_gc: Option<bool>,
    ) -> PyResult<Self> {
        let mut options = Options::default();
        if let Some(client_id) = client_id {
            options.client_id = client_id;
        }

        if let Some(raw_offset) = offset_kind {
            let clean_offset = raw_offset.to_lowercase().replace("-", "");
            let offset = match clean_offset.as_str() {
                "utf8" => Ok(OffsetKind::Bytes),
                "utf16" => Ok(OffsetKind::Utf16),
                "utf32" => Ok(OffsetKind::Utf32),
                _ => Err(pyo3::exceptions::PyValueError::new_err(format!(
                    "'{}' is not a valid offset kind (utf8, utf16, or utf32).",
                    clean_offset
                ))),
            }?;
            options.offset_kind = offset;
        }

        if let Some(skip_gc) = skip_gc {
            options.skip_gc = skip_gc;
        }

        Ok(YDoc(Doc::with_options(options)))
    }

    /// Gets globally unique identifier of this `YDoc` instance.
    #[getter]
    pub fn id(&self) -> f64 {
        self.0.client_id as f64
    }

    /// begin_transaction(/)
    /// --
    ///
    /// Returns a new transaction for this document. y-py shared data types execute their
    /// operations in a context of a given transaction. Each document can have only one active
    /// transaction at the time - subsequent attempts will cause exception to be thrown.
    ///
    /// Transactions started with `doc.begin_transaction` can be released by deleting the transaction object
    /// method.
    ///
    /// Example:
    ///
    /// ```python
    /// from y_py import YDoc
    /// doc = YDoc()
    /// text = doc.get_text('name')
    /// with doc.begin_transaction() as txn:
    ///     text.insert(txn, 0, 'hello world')
    /// ```
    pub fn begin_transaction(&mut self) -> YTransaction {
        YTransaction(self.0.transact())
    }

    pub fn transact(&mut self, callback: PyObject) -> PyResult<PyObject> {
        let txn = self.begin_transaction();
        Python::with_gil(|py| {
            let args = PyTuple::new(py, std::iter::once(txn.into_py(py)));
            callback.call(py, args, None)
        })
    }

    /// Returns a `YMap` shared data type, that's accessible for subsequent accesses using given
    /// `name`.
    ///
    /// If there was no instance with this name before, it will be created and then returned.
    ///
    /// If there was an instance with this name, but it was of different type, it will be projected
    /// onto `YMap` instance.
    pub fn get_map(&mut self, name: &str) -> YMap {
        self.begin_transaction().get_map(name)
    }

    /// Returns a `YXmlElement` shared data type, that's accessible for subsequent accesses using
    /// given `name`.
    ///
    /// If there was no instance with this name before, it will be created and then returned.
    ///
    /// If there was an instance with this name, but it was of different type, it will be projected
    /// onto `YXmlElement` instance.
    pub fn get_xml_element(&mut self, name: &str) -> YXmlElement {
        YXmlElement(self.begin_transaction().get_xml_element(name))
    }

    /// Returns a `YXmlText` shared data type, that's accessible for subsequent accesses using given
    /// `name`.
    ///
    /// If there was no instance with this name before, it will be created and then returned.
    ///
    /// If there was an instance with this name, but it was of different type, it will be projected
    /// onto `YXmlText` instance.
    pub fn get_xml_text(&mut self, name: &str) -> YXmlText {
        YXmlText(self.begin_transaction().get_xml_text(name))
    }

    /// Returns a `YArray` shared data type, that's accessible for subsequent accesses using given
    /// `name`.
    ///
    /// If there was no instance with this name before, it will be created and then returned.
    ///
    /// If there was an instance with this name, but it was of different type, it will be projected
    /// onto `YArray` instance.
    pub fn get_array(&mut self, name: &str) -> YArray {
        self.begin_transaction().get_array(name)
    }

    /// Returns a `YText` shared data type, that's accessible for subsequent accesses using given
    /// `name`.
    ///
    /// If there was no instance with this name before, it will be created and then returned.
    ///
    /// If there was an instance with this name, but it was of different type, it will be projected
    /// onto `YText` instance.
    pub fn get_text(&mut self, name: &str) -> YText {
        self.begin_transaction().get_text(name)
    }
}

/// Encodes a state vector of a given y-py document into its binary representation using lib0 v1
/// encoding. State vector is a compact representation of updates performed on a given document and
/// can be used by `encode_state_as_update` on remote peer to generate a delta update payload to
/// synchronize changes between peers.
///
/// Example:
///
/// ```python
/// from y_py import YDoc, encode_state_vector, encode_state_as_update, apply_update from y_py
///
/// # document on machine A
/// local_doc = YDoc()
/// local_sv = encode_state_vector(local_doc)
///
/// # document on machine B
/// remote_doc = YDoc()
/// remote_delta = encode_state_as_update(remote_doc, local_sv)
///
/// apply_update(local_doc, remote_delta)
/// ```
#[pyfunction]
pub fn encode_state_vector(doc: &mut YDoc) -> Vec<u8> {
    doc.begin_transaction().state_vector_v1()
}

/// Encodes all updates that have happened since a given version `vector` into a compact delta
/// representation using lib0 v1 encoding. If `vector` parameter has not been provided, generated
/// delta payload will contain all changes of a current y-py document, working effectively as its
/// state snapshot.
///
/// Example:
///
/// ```python
/// from y_py import YDoc, encode_state_vector, encode_state_as_update, apply_update
///
/// # document on machine A
/// local_doc = YDoc()
/// local_sv = encode_state_vector(local_doc)
///
/// # document on machine B
/// remote_doc = YDoc()
/// remote_delta = encode_state_as_update(remote_doc, local_sv)
///
/// apply_update(local_doc, remote_delta)
/// ```
#[pyfunction]
pub fn encode_state_as_update(doc: &mut YDoc, vector: Option<Vec<u8>>) -> Vec<u8> {
    doc.begin_transaction().diff_v1(vector)
}

/// Applies delta update generated by the remote document replica to a current document. This
/// method assumes that a payload maintains lib0 v1 encoding format.
///
/// Example:
///
/// ```python
/// from y_py import YDoc, encode_state_vector, encode_state_as_update, apply_update
///
/// # document on machine A
/// local_doc = YDoc()
/// local_sv = encode_state_vector(local_doc)
///
/// # document on machine B
/// remote_doc = YDoc()
/// remote_delta = encode_state_as_update(remote_doc, local_sv)
///
/// apply_update(local_doc, remote_delta)
/// ```
#[pyfunction]
pub fn apply_update(doc: &mut YDoc, diff: Vec<u8>) {
    doc.begin_transaction().apply_v1(diff);
}

/// A transaction that serves as a proxy to document block store. y-py shared data types execute
/// their operations in a context of a given transaction. Each document can have only one active
/// transaction at the time - subsequent attempts will cause exception to be thrown.
///
/// Transactions started with `doc.begin_transaction` can be released by deleting the transaction object
/// method.
///
/// Example:
///
/// ```python
/// from y_py import YDoc
/// doc = YDoc()
/// text = doc.get_text('name')
/// with doc.begin_transaction() as txn:
///     text.insert(txn, 0, 'hello world')
/// ```
#[pyclass(unsendable)]
pub struct YTransaction(Transaction);

impl Deref for YTransaction {
    type Target = Transaction;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for YTransaction {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

#[pymethods]
impl YTransaction {
    /// Returns a `YText` shared data type, that's accessible for subsequent accesses using given
    /// `name`.
    ///
    /// If there was no instance with this name before, it will be created and then returned.
    ///
    /// If there was an instance with this name, but it was of different type, it will be projected
    /// onto `YText` instance.
    pub fn get_text(&mut self, name: &str) -> YText {
        self.0.get_text(name).into()
    }

    /// Returns a `YArray` shared data type, that's accessible for subsequent accesses using given
    /// `name`.
    ///
    /// If there was no instance with this name before, it will be created and then returned.
    ///
    /// If there was an instance with this name, but it was of different type, it will be projected
    /// onto `YArray` instance.
    pub fn get_array(&mut self, name: &str) -> YArray {
        self.0.get_array(name).into()
    }

    /// Returns a `YMap` shared data type, that's accessible for subsequent accesses using given
    /// `name`.
    ///
    /// If there was no instance with this name before, it will be created and then returned.
    ///
    /// If there was an instance with this name, but it was of different type, it will be projected
    /// onto `YMap` instance.
    pub fn get_map(&mut self, name: &str) -> YMap {
        self.0.get_map(name).into()
    }

    /// Triggers a post-update series of operations without `free`ing the transaction. This includes
    /// compaction and optimization of internal representation of updates, triggering events etc.
    /// y-py transactions are auto-committed when they are `free`d.
    pub fn commit(&mut self) {
        self.0.commit()
    }

    /// Encodes a state vector of a given transaction document into its binary representation using
    /// lib0 v1 encoding. State vector is a compact representation of updates performed on a given
    /// document and can be used by `encode_state_as_update` on remote peer to generate a delta
    /// update payload to synchronize changes between peers.
    ///
    /// Example:
    ///
    /// ```python
    /// from y_py import YDoc
    ///
    /// # document on machine A
    /// local_doc = YDoc()
    /// local_txn = local_doc.begin_transaction()
    ///
    /// # document on machine B
    /// remote_doc = YDoc()
    /// remote_txn = local_doc.begin_transaction()
    ///
    /// try:
    ///     local_sv = local_txn.state_vector_v1()
    ///     remote_delta = remote_txn.diff_v1(local_sv)
    ///     local_txn.applyV1(remote_delta)
    /// finally:
    ///     del local_txn
    ///     del remote_txn
    ///
    /// ```
    pub fn state_vector_v1(&self) -> Vec<u8> {
        let sv = self.0.state_vector();
        let payload = sv.encode_v1();
        payload
    }

    /// Encodes all updates that have happened since a given version `vector` into a compact delta
    /// representation using lib0 v1 encoding. If `vector` parameter has not been provided, generated
    /// delta payload will contain all changes of a current y-py document, working effectively as
    /// its state snapshot.
    ///
    /// Example:
    ///
    /// ```python
    /// from y_py import YDoc
    ///
    /// # document on machine A
    /// local_doc = YDoc()
    /// local_txn = local_doc.begin_transaction()
    ///
    /// # document on machine B
    /// remote_doc = YDoc()
    /// remote_txn = local_doc.begin_transaction()
    ///
    /// try:
    ///     local_sv = local_txn.state_vector_v1()
    ///     remote_delta = remote_txn.diff_v1(local_sv)
    ///     local_txn.applyV1(remote_delta)
    /// finally:
    ///     del local_txn
    ///     del remote_txn
    /// ```
    pub fn diff_v1(&self, vector: Option<Vec<u8>>) -> Vec<u8> {
        let mut encoder = EncoderV1::new();
        let sv = if let Some(vector) = vector {
            StateVector::decode_v1(vector.to_vec().as_slice())
        } else {
            StateVector::default()
        };
        self.0.encode_diff(&sv, &mut encoder);
        encoder.to_vec()
    }

    /// Applies delta update generated by the remote document replica to a current transaction's
    /// document. This method assumes that a payload maintains lib0 v1 encoding format.
    ///
    /// Example:
    ///
    /// ```python
    /// from y_py import YDoc
    ///
    /// # document on machine A
    /// local_doc = YDoc()
    /// local_txn = local_doc.begin_transaction()
    ///
    /// # document on machine B
    /// remote_doc = YDoc()
    /// remote_txn = local_doc.begin_transaction()
    ///
    /// try:
    ///     local_sv = local_txn.state_vector_v1()
    ///     remote_delta = remote_txn.diff_v1(local_sv)
    ///     local_txn.applyV1(remote_delta)
    /// finally:
    ///     del local_txn
    ///     del remote_txn
    /// ```
    pub fn apply_v1(&mut self, diff: Vec<u8>) {
        let diff: Vec<u8> = diff.to_vec();
        let mut decoder = DecoderV1::from(diff.as_slice());
        let update = Update::decode(&mut decoder);
        self.0.apply_update(update)
    }

    /// Allows YTransaction to be used with a Python context block.
    ///
    /// Example
    /// ```python
    /// from y_py import YDoc
    ///
    /// doc = YDoc()
    ///
    /// with doc.begin_transaction() as txn:
    ///     # Perform updates within this block
    ///
    /// ```
    fn __enter__<'p>(slf: PyRef<'p, Self>, _py: Python<'p>) -> PyResult<PyRef<'p, Self>> {
        Ok(slf)
    }

    /// Allows YTransaction to be used with a Python context block.
    /// Commits the results when the `with` context closes.
    ///
    /// Example
    /// ```python
    /// from y_py import YDoc
    ///
    /// doc = YDoc()
    ///
    /// with doc.begin_transaction() as txn:
    ///     # Updates
    /// # Commit is called here when the context exits
    ///
    /// ```
    fn __exit__<'p>(
        &'p mut self,
        _exc_type: Option<&'p PyAny>,
        _exc_value: Option<&'p PyAny>,
        _traceback: Option<&'p PyAny>,
    ) -> PyResult<bool> {
        self.commit();
        drop(self);
        return Ok(true);
    }
}

#[derive(Clone)]
enum SharedType<T, P> {
    Integrated(T),
    Prelim(P),
}

impl<T, P> SharedType<T, P> {
    #[inline(always)]
    fn new(value: T) -> Self {
        SharedType::Integrated(value)
    }

    #[inline(always)]
    fn prelim(prelim: P) -> Self {
        SharedType::Prelim(prelim)
    }
}

/// A shared data type used for collaborative text editing. It enables multiple users to add and
/// remove chunks of text in efficient manner. This type is internally represented as a mutable
/// double-linked list of text chunks - an optimization occurs during `YTransaction.commit`, which
/// allows to squash multiple consecutively inserted characters together as a single chunk of text
/// even between transaction boundaries in order to preserve more efficient memory model.
///
/// `YText` structure internally uses UTF-8 encoding and its length is described in a number of
/// bytes rather than individual characters (a single UTF-8 code point can consist of many bytes).
///
/// Like all Yrs shared data types, `YText` is resistant to the problem of interleaving (situation
/// when characters inserted one after another may interleave with other peers concurrent inserts
/// after merging all updates together). In case of Yrs conflict resolution is solved by using
/// unique document id to determine correct and consistent ordering.
#[pyclass(unsendable)]
#[derive(Clone)]
pub struct YText(SharedType<Text, String>);
impl From<Text> for YText {
    fn from(v: Text) -> Self {
        YText(SharedType::new(v))
    }
}

#[pymethods]
impl YText {
    /// Creates a new preliminary instance of a `YText` shared data type, with its state initialized
    /// to provided parameter.
    ///
    /// Preliminary instances can be nested into other shared data types such as `YArray` and `YMap`.
    /// Once a preliminary instance has been inserted this way, it becomes integrated into y-py
    /// document store and cannot be nested again: attempt to do so will result in an exception.
    #[new]
    pub fn new(init: Option<String>) -> Self {
        YText(SharedType::prelim(init.unwrap_or_default()))
    }

    /// Returns true if this is a preliminary instance of `YText`.
    ///
    /// Preliminary instances can be nested into other shared data types such as `YArray` and `YMap`.
    /// Once a preliminary instance has been inserted this way, it becomes integrated into y-py
    /// document store and cannot be nested again: attempt to do so will result in an exception.
    #[getter]
    pub fn prelim(&self) -> bool {
        match self.0 {
            SharedType::Prelim(_) => true,
            _ => false,
        }
    }

    /// Returns length of an underlying string stored in this `YText` instance,
    /// understood as a number of UTF-8 encoded bytes.
    #[getter]
    pub fn length(&self) -> u32 {
        match &self.0 {
            SharedType::Integrated(v) => v.len(),
            SharedType::Prelim(v) => v.len() as u32,
        }
    }

    /// Returns an underlying shared string stored in this data type.
    pub fn to_string(&self, txn: &YTransaction) -> String {
        match &self.0 {
            SharedType::Integrated(v) => v.to_string(txn),
            SharedType::Prelim(v) => v.clone(),
        }
    }

    /// Returns an underlying shared string stored in this data type.
    pub fn to_json(&self, txn: &YTransaction) -> String {
        match &self.0 {
            SharedType::Integrated(v) => v.to_string(txn),
            SharedType::Prelim(v) => v.clone(),
        }
    }

    /// Inserts a given `chunk` of text into this `YText` instance, starting at a given `index`.
    pub fn insert(&mut self, txn: &mut YTransaction, index: u32, chunk: &str) {
        match &mut self.0 {
            SharedType::Integrated(v) => v.insert(txn, index, chunk),
            SharedType::Prelim(v) => v.insert_str(index as usize, chunk),
        }
    }

    /// Appends a given `chunk` of text at the end of current `YText` instance.
    pub fn push(&mut self, txn: &mut YTransaction, chunk: &str) {
        match &mut self.0 {
            SharedType::Integrated(v) => v.push(txn, chunk),
            SharedType::Prelim(v) => v.push_str(chunk),
        }
    }

    /// Deletes a specified range of of characters, starting at a given `index`.
    /// Both `index` and `length` are counted in terms of a number of UTF-8 character bytes.
    pub fn delete(&mut self, txn: &mut YTransaction, index: u32, length: u32) {
        match &mut self.0 {
            SharedType::Integrated(v) => v.remove_range(txn, index, length),
            SharedType::Prelim(v) => {
                v.drain((index as usize)..(index + length) as usize);
            }
        }
    }
}

/// A collection used to store data in an indexed sequence structure. This type is internally
/// implemented as a double linked list, which may squash values inserted directly one after another
/// into single list node upon transaction commit.
///
/// Reading a root-level type as an YArray means treating its sequence components as a list, where
/// every countable element becomes an individual entity:
///
/// - JSON-like primitives (booleans, numbers, strings, JSON maps, arrays etc.) are counted
///   individually.
/// - Text chunks inserted by [Text] data structure: each character becomes an element of an
///   array.
/// - Embedded and binary values: they count as a single element even though they correspond of
///   multiple bytes.
///
/// Like all Yrs shared data types, YArray is resistant to the problem of interleaving (situation
/// when elements inserted one after another may interleave with other peers concurrent inserts
/// after merging all updates together). In case of Yrs conflict resolution is solved by using
/// unique document id to determine correct and consistent ordering.
#[pyclass(unsendable)]
pub struct YArray(SharedType<Array, Vec<PyObject>>);

impl From<Array> for YArray {
    fn from(v: Array) -> Self {
        YArray(SharedType::new(v))
    }
}

#[pymethods]
impl YArray {
    /// Creates a new preliminary instance of a `YArray` shared data type, with its state
    /// initialized to provided parameter.
    ///
    /// Preliminary instances can be nested into other shared data types such as `YArray` and `YMap`.
    /// Once a preliminary instance has been inserted this way, it becomes integrated into y-py
    /// document store and cannot be nested again: attempt to do so will result in an exception.
    #[new]
    pub fn new(init: Option<Vec<PyObject>>) -> Self {
        YArray(SharedType::prelim(init.unwrap_or_default()))
    }

    /// Returns true if this is a preliminary instance of `YArray`.
    ///
    /// Preliminary instances can be nested into other shared data types such as `YArray` and `YMap`.
    /// Once a preliminary instance has been inserted this way, it becomes integrated into y-py
    /// document store and cannot be nested again: attempt to do so will result in an exception.
    #[getter]
    pub fn prelim(&self) -> bool {
        match &self.0 {
            SharedType::Prelim(_) => true,
            _ => false,
        }
    }

    /// Returns a number of elements stored within this instance of `YArray`.
    #[getter]
    pub fn length(&self) -> u32 {
        match &self.0 {
            SharedType::Integrated(v) => v.len(),
            SharedType::Prelim(v) => v.len() as u32,
        }
    }

    /// Converts an underlying contents of this `YArray` instance into their JSON representation.
    pub fn to_json(&self, txn: &YTransaction) -> PyObject {
        Python::with_gil(|py| match &self.0 {
            SharedType::Integrated(v) => AnyWrapper(v.to_json(txn)).into_py(py),
            SharedType::Prelim(v) => {
                let py_ptrs: Vec<PyObject> = v.iter().cloned().collect();
                py_ptrs.into_py(py)
            }
        })
    }

    /// Inserts a given range of `items` into this `YArray` instance, starting at given `index`.
    pub fn insert(&mut self, txn: &mut YTransaction, index: u32, items: Vec<PyObject>) {
        let mut j = index;
        match &mut self.0 {
            SharedType::Integrated(array) => {
                insert_at(array, txn, index, items);
            }
            SharedType::Prelim(vec) => {
                for el in items {
                    vec.insert(j as usize, el);
                    j += 1;
                }
            }
        }
    }

    /// Appends a range of `items` at the end of this `YArray` instance.
    pub fn push(&mut self, txn: &mut YTransaction, items: Vec<PyObject>) {
        let index = self.length();
        self.insert(txn, index, items);
    }

    /// Deletes a range of items of given `length` from current `YArray` instance,
    /// starting from given `index`.
    pub fn delete(&mut self, txn: &mut YTransaction, index: u32, length: u32) {
        match &mut self.0 {
            SharedType::Integrated(v) => v.remove_range(txn, index, length),
            SharedType::Prelim(v) => {
                v.drain((index as usize)..(index + length) as usize);
            }
        }
    }

    /// Returns an element stored under given `index`.
    pub fn get(&self, txn: &YTransaction, index: u32) -> PyResult<PyObject> {
        match &self.0 {
            SharedType::Integrated(v) => {
                if let Some(value) = v.get(txn, index) {
                    Ok(Python::with_gil(|py| ValueWrapper(value).into_py(py)))
                } else {
                    Err(PyIndexError::new_err(
                        "Index outside the bounds of an YArray",
                    ))
                }
            }
            SharedType::Prelim(v) => {
                if let Some(value) = v.get(index as usize) {
                    Ok(value.clone())
                } else {
                    Err(PyIndexError::new_err(
                        "Index outside the bounds of an YArray",
                    ))
                }
            }
        }
    }

    /// Returns an iterator that can be used to traverse over the values stored withing this
    /// instance of `YArray`.
    ///
    /// Example:
    ///
    /// ```python
    /// from y_py import YDoc
    ///
    /// # document on machine A
    /// doc = YDoc()
    /// array = doc.get_array('name')
    ///
    /// with doc.begin_transaction() as txn:
    ///     array.push(txn, ['hello', 'world'])
    ///     for item in array.values(txn)):
    ///         print(item)
    /// ```
    pub fn values(&self, txn: &YTransaction) -> YArrayIterator {
        let inner_iter = match &self.0 {
            SharedType::Integrated(v) => unsafe {
                let this: *const Array = v;
                let tx: *const Transaction = txn.deref() as *const _;
                InnerYArrayIter::Integrated((*this).iter(tx.as_ref().unwrap()))
            },
            SharedType::Prelim(v) => unsafe {
                let this: *const Vec<PyObject> = v;
                InnerYArrayIter::Prelim((*this).iter())
            },
        };
        YArrayIterator(ManuallyDrop::new(inner_iter))
    }
}

enum InnerYArrayIter {
    Integrated(ArrayIter<'static>),
    Prelim(std::slice::Iter<'static, PyObject>),
}

#[pyclass(unsendable)]
pub struct YArrayIterator(ManuallyDrop<InnerYArrayIter>);

impl Drop for YArrayIterator {
    fn drop(&mut self) {
        unsafe { ManuallyDrop::drop(&mut self.0) }
    }
}

#[pymethods]
impl YArrayIterator {
    pub fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }

    pub fn __next__(mut slf: PyRefMut<Self>) -> Option<PyObject> {
        match slf.0.deref_mut() {
            InnerYArrayIter::Integrated(iter) => {
                Python::with_gil(|py| iter.next().map(|v| ValueWrapper(v).into_py(py)))
            }
            InnerYArrayIter::Prelim(iter) => iter.next().cloned(),
        }
    }
}

/// Collection used to store key-value entries in an unordered manner. Keys are always represented
/// as UTF-8 strings. Values can be any value type supported by Yrs: JSON-like primitives as well as
/// shared data types.
///
/// In terms of conflict resolution, [Map] uses logical last-write-wins principle, meaning the past
/// updates are automatically overridden and discarded by newer ones, while concurrent updates made
/// by different peers are resolved into a single value using document id seniority to establish
/// order.
#[pyclass(unsendable)]
pub struct YMap(SharedType<Map, HashMap<String, PyObject>>);

impl From<Map> for YMap {
    fn from(v: Map) -> Self {
        YMap(SharedType::new(v))
    }
}

#[pymethods]
impl YMap {
    /// Creates a new preliminary instance of a `YMap` shared data type, with its state
    /// initialized to provided parameter.
    ///
    /// Preliminary instances can be nested into other shared data types such as `YArray` and `YMap`.
    /// Once a preliminary instance has been inserted this way, it becomes integrated into y-py
    /// document store and cannot be nested again: attempt to do so will result in an exception.
    #[new]
    pub fn new(dict: &PyDict) -> PyResult<Self> {
        let mut map: HashMap<String, PyObject> = HashMap::new();
        for (k, v) in dict.iter() {
            let k = k.downcast::<pyo3::types::PyString>()?.to_string();
            let v: PyObject = v.into();
            map.insert(k, v);
        }
        Ok(YMap(SharedType::Prelim(map)))
    }

    /// Returns true if this is a preliminary instance of `YMap`.
    ///
    /// Preliminary instances can be nested into other shared data types such as `YArray` and `YMap`.
    /// Once a preliminary instance has been inserted this way, it becomes integrated into y-py
    /// document store and cannot be nested again: attempt to do so will result in an exception.
    #[getter]
    pub fn prelim(&self) -> bool {
        match &self.0 {
            SharedType::Prelim(_) => true,
            _ => false,
        }
    }

    /// Returns a number of entries stored within this instance of `YMap`.
    pub fn length(&self, txn: &YTransaction) -> u32 {
        match &self.0 {
            SharedType::Integrated(v) => v.len(txn),
            SharedType::Prelim(v) => v.len() as u32,
        }
    }

    /// Converts contents of this `YMap` instance into a JSON representation.
    pub fn to_json(&self, txn: &YTransaction) -> PyResult<PyObject> {
        Python::with_gil(|py| match &self.0 {
            SharedType::Integrated(v) => Ok(AnyWrapper(v.to_json(txn)).into_py(py)),
            SharedType::Prelim(v) => {
                let dict = PyDict::new(py);
                for (k, v) in v.iter() {
                    dict.set_item(k, v)?;
                }
                Ok(dict.into())
            }
        })
    }

    /// Sets a given `key`-`value` entry within this instance of `YMap`. If another entry was
    /// already stored under given `key`, it will be overridden with new `value`.
    pub fn set(&mut self, txn: &mut YTransaction, key: &str, value: PyObject) {
        match &mut self.0 {
            SharedType::Integrated(v) => {
                v.insert(txn, key.to_string(), PyValueWrapper(value));
            }
            SharedType::Prelim(v) => {
                v.insert(key.to_string(), value);
            }
        }
    }

    /// Removes an entry identified by a given `key` from this instance of `YMap`, if such exists.
    pub fn delete(&mut self, txn: &mut YTransaction, key: &str) {
        match &mut self.0 {
            SharedType::Integrated(v) => {
                v.remove(txn, key);
            }
            SharedType::Prelim(v) => {
                v.remove(key);
            }
        }
    }

    /// Returns value of an entry stored under given `key` within this instance of `YMap`,
    /// or `undefined` if no such entry existed.
    pub fn get(&self, txn: &mut YTransaction, key: &str) -> PyObject {
        match &self.0 {
            SharedType::Integrated(v) => Python::with_gil(|py| {
                if let Some(value) = v.get(txn, key) {
                    ValueWrapper(value).into_py(py)
                } else {
                    py.None()
                }
            }),
            SharedType::Prelim(v) => {
                if let Some(value) = v.get(key) {
                    value.clone()
                } else {
                    Python::with_gil(|py| py.None())
                }
            }
        }
    }

    /// entries(self, txn)
    /// --
    ///
    /// Returns an iterator that can be used to traverse over all entries stored within this
    /// instance of `YMap`. Order of entry is not specified.
    ///
    /// Example:
    ///
    /// ```python
    /// from y_py import YDoc
    ///
    /// # document on machine A
    /// doc = YDoc()
    /// map = doc.get_map('name')
    /// with doc.begin_transaction() as txn:
    ///     map.set(txn, 'key1', 'value1')
    ///     map.set(txn, 'key2', true)
    ///     for (key, value) in map.entries(txn)):
    ///         print(key, value)
    /// ```
    pub fn entries(&self, txn: &mut YTransaction) -> YMapIterator {
        match &self.0 {
            SharedType::Integrated(val) => unsafe {
                let this: *const Map = val;
                let tx: *const Transaction = &txn.0 as *const _;
                let shared_iter =
                    SharedYMapIterator::Integrated((*this).iter(tx.as_ref().unwrap()));
                YMapIterator(ManuallyDrop::new(shared_iter))
            },
            SharedType::Prelim(val) => unsafe {
                let this: *const HashMap<String, PyObject> = val;
                let shared_iter = SharedYMapIterator::Prelim((*this).iter());
                YMapIterator(ManuallyDrop::new(shared_iter))
            },
        }
    }
}

pub enum SharedYMapIterator {
    Integrated(MapIter<'static>),
    Prelim(std::collections::hash_map::Iter<'static, String, PyObject>),
}

#[pyclass(unsendable)]
pub struct YMapIterator(ManuallyDrop<SharedYMapIterator>);

impl Drop for YMapIterator {
    fn drop(&mut self) {
        unsafe { ManuallyDrop::drop(&mut self.0) }
    }
}

#[pyproto]
impl<'p> PyIterProtocol for YMapIterator {
    fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }
    fn __next__(mut slf: PyRefMut<Self>) -> Option<(String, PyObject)> {
        match slf.0.deref_mut() {
            SharedYMapIterator::Integrated(iter) => Python::with_gil(|py| {
                iter.next()
                    .map(|(k, v)| (k.to_string(), ValueWrapper(v).into_py(py)))
            }),
            SharedYMapIterator::Prelim(iter) => iter.next().map(|(k, v)| (k.clone(), v.clone())),
        }
    }
}

/// XML element data type. It represents an XML node, which can contain key-value attributes
/// (interpreted as strings) as well as other nested XML elements or rich text (represented by
/// `YXmlText` type).
///
/// In terms of conflict resolution, `YXmlElement` uses following rules:
///
/// - Attribute updates use logical last-write-wins principle, meaning the past updates are
///   automatically overridden and discarded by newer ones, while concurrent updates made by
///   different peers are resolved into a single value using document id seniority to establish
///   an order.
/// - Child node insertion uses sequencing rules from other Yrs collections - elements are inserted
///   using interleave-resistant algorithm, where order of concurrent inserts at the same index
///   is established using peer's document id seniority.
#[pyclass(unsendable)]
pub struct YXmlElement(XmlElement);

#[pymethods]
impl YXmlElement {
    /// Returns a tag name of this XML node.
    #[getter]
    pub fn name(&self) -> String {
        self.0.tag().to_string()
    }

    /// Returns a number of child XML nodes stored within this `YXMlElement` instance.
    pub fn length(&self, txn: &YTransaction) -> u32 {
        self.0.len(txn)
    }

    /// Inserts a new instance of `YXmlElement` as a child of this XML node and returns it.
    pub fn insert_xml_element(
        &self,
        txn: &mut YTransaction,
        index: u32,
        name: &str,
    ) -> YXmlElement {
        YXmlElement(self.0.insert_elem(txn, index, name))
    }

    /// Inserts a new instance of `YXmlText` as a child of this XML node and returns it.
    pub fn insert_xml_text(&self, txn: &mut YTransaction, index: u32) -> YXmlText {
        YXmlText(self.0.insert_text(txn, index))
    }

    /// Removes a range of children XML nodes from this `YXmlElement` instance,
    /// starting at given `index`.
    pub fn delete(&self, txn: &mut YTransaction, index: u32, length: u32) {
        self.0.remove_range(txn, index, length)
    }

    /// Appends a new instance of `YXmlElement` as the last child of this XML node and returns it.
    pub fn push_xml_element(&self, txn: &mut YTransaction, name: &str) -> YXmlElement {
        YXmlElement(self.0.push_elem_back(txn, name))
    }

    /// Appends a new instance of `YXmlText` as the last child of this XML node and returns it.
    pub fn push_xml_text(&self, txn: &mut YTransaction) -> YXmlText {
        YXmlText(self.0.push_text_back(txn))
    }

    /// Returns a first child of this XML node.
    /// It can be either `YXmlElement`, `YXmlText` or `undefined` if current node has not children.
    pub fn first_child(&self, txn: &YTransaction) -> PyObject {
        Python::with_gil(|py| {
            self.0
                .first_child(txn)
                .map_or(py.None(), |xml| XmlWrapper(xml).into_py(py))
        })
    }

    /// Returns a next XML sibling node of this XMl node.
    /// It can be either `YXmlElement`, `YXmlText` or `undefined` if current node is a last child of
    /// parent XML node.
    pub fn next_sibling(&self, txn: &YTransaction) -> PyObject {
        Python::with_gil(|py| {
            self.0
                .next_sibling(txn)
                .map_or(py.None(), |xml| XmlWrapper(xml).into_py(py))
        })
    }

    /// Returns a previous XML sibling node of this XMl node.
    /// It can be either `YXmlElement`, `YXmlText` or `undefined` if current node is a first child
    /// of parent XML node.
    pub fn prev_sibling(&self, txn: &YTransaction) -> PyObject {
        Python::with_gil(|py| self.0.prev_sibling(txn).map_or(py.None(), xml_into_py))
    }

    /// Returns a parent `YXmlElement` node or `undefined` if current node has no parent assigned.
    pub fn parent(&self, txn: &YTransaction) -> Option<YXmlElement> {
        self.0.parent(txn).map(YXmlElement)
    }

    /// Returns a string representation of this XML node.
    pub fn to_string(&self, txn: &YTransaction) -> String {
        self.0.to_string(txn)
    }

    /// Sets a `name` and `value` as new attribute for this XML node. If an attribute with the same
    /// `name` already existed on that node, its value with be overridden with a provided one.
    pub fn set_attribute(&self, txn: &mut YTransaction, name: &str, value: &str) {
        self.0.insert_attribute(txn, name, value)
    }

    /// Returns a value of an attribute given its `name`. If no attribute with such name existed,
    /// `null` will be returned.
    pub fn get_attribute(&self, txn: &YTransaction, name: &str) -> Option<String> {
        self.0.get_attribute(txn, name)
    }

    /// Removes an attribute from this XML node, given its `name`.
    pub fn remove_attribute(&self, txn: &mut YTransaction, name: &str) {
        self.0.remove_attribute(txn, &name);
    }

    /// Returns an iterator that enables to traverse over all attributes of this XML node in
    /// unspecified order.
    pub fn attributes(&self, txn: &YTransaction) -> YXmlAttributes {
        unsafe {
            let this: *const XmlElement = &self.0;
            let tx: *const Transaction = txn.deref() as *const _;
            let static_iter: ManuallyDrop<Attributes<'static>> =
                ManuallyDrop::new((*this).attributes(tx.as_ref().unwrap()));
            YXmlAttributes(static_iter)
        }
    }

    /// Returns an iterator that enables a deep traversal of this XML node - starting from first
    /// child over this XML node successors using depth-first strategy.
    pub fn tree_walker(&self, txn: &YTransaction) -> YXmlTreeWalker {
        unsafe {
            let this: *const XmlElement = &self.0;
            let tx: *const Transaction = txn.deref() as *const _;
            let static_iter: ManuallyDrop<TreeWalker<'static>> =
                ManuallyDrop::new((*this).successors(tx.as_ref().unwrap()));
            YXmlTreeWalker(static_iter)
        }
    }

    /// Subscribes to all operations happening over this instance of `YXmlElement`. All changes are
    /// batched and eventually triggered during transaction commit phase.
    /// Returns an `YXmlObserver` which, when free'd, will unsubscribe current callback.
    pub fn observe(&mut self, f: PyObject) -> YXmlObserver {
        self.0
            .observe(move |txn, e| {
                Python::with_gil(|py| {
                    let event = YXmlEvent::new(e, txn);
                    f.call1(py, (event,)).unwrap();
                })
            })
            .into()
    }
}

/// A shared data type used for collaborative text editing, that can be used in a context of
/// `YXmlElement` nodee. It enables multiple users to add and remove chunks of text in efficient
/// manner. This type is internally represented as a mutable double-linked list of text chunks
/// - an optimization occurs during `YTransaction.commit`, which allows to squash multiple
/// consecutively inserted characters together as a single chunk of text even between transaction
/// boundaries in order to preserve more efficient memory model.
///
/// Just like `YXmlElement`, `YXmlText` can be marked with extra metadata in form of attributes.
///
/// `YXmlText` structure internally uses UTF-8 encoding and its length is described in a number of
/// bytes rather than individual characters (a single UTF-8 code point can consist of many bytes).
///
/// Like all Yrs shared data types, `YXmlText` is resistant to the problem of interleaving (situation
/// when characters inserted one after another may interleave with other peers concurrent inserts
/// after merging all updates together). In case of Yrs conflict resolution is solved by using
/// unique document id to determine correct and consistent ordering.
#[pyclass(unsendable)]
pub struct YXmlText(XmlText);

#[pymethods]
impl YXmlText {
    /// Returns length of an underlying string stored in this `YXmlText` instance,
    /// understood as a number of UTF-8 encoded bytes.
    #[getter]
    pub fn length(&self) -> u32 {
        self.0.len()
    }

    /// Inserts a given `chunk` of text into this `YXmlText` instance, starting at a given `index`.
    pub fn insert(&self, txn: &mut YTransaction, index: i32, chunk: &str) {
        self.0.insert(txn, index as u32, chunk)
    }

    /// Appends a given `chunk` of text at the end of `YXmlText` instance.
    pub fn push(&self, txn: &mut YTransaction, chunk: &str) {
        self.0.push(txn, chunk)
    }

    /// Deletes a specified range of of characters, starting at a given `index`.
    /// Both `index` and `length` are counted in terms of a number of UTF-8 character bytes.
    pub fn delete(&self, txn: &mut YTransaction, index: u32, length: u32) {
        self.0.remove_range(txn, index, length)
    }

    /// Returns a next XML sibling node of this XMl node.
    /// It can be either `YXmlElement`, `YXmlText` or `undefined` if current node is a last child of
    /// parent XML node.
    pub fn next_sibling(&self, txn: &YTransaction) -> PyObject {
        if let Some(xml) = self.0.next_sibling(txn) {
            xml_into_py(xml)
        } else {
            Python::with_gil(|py| py.None())
        }
    }

    /// Returns a previous XML sibling node of this XMl node.
    /// It can be either `YXmlElement`, `YXmlText` or `undefined` if current node is a first child
    /// of parent XML node.
    pub fn prev_sibling(&self, txn: &YTransaction) -> PyObject {
        if let Some(xml) = self.0.prev_sibling(txn) {
            xml_into_py(xml)
        } else {
            Python::with_gil(|py| py.None())
        }
    }

    /// Returns a parent `YXmlElement` node or `undefined` if current node has no parent assigned.
    pub fn parent(&self, txn: &YTransaction) -> PyObject {
        if let Some(xml) = self.0.parent(txn) {
            xml_into_py(Xml::Element(xml))
        } else {
            Python::with_gil(|py| py.None())
        }
    }

    /// Returns an underlying string stored in this `YXmlText` instance.
    pub fn to_string(&self, txn: &YTransaction) -> String {
        self.0.to_string(txn)
    }

    /// Sets a `name` and `value` as new attribute for this XML node. If an attribute with the same
    /// `name` already existed on that node, its value with be overridden with a provided one.
    pub fn set_attribute(&self, txn: &mut YTransaction, name: &str, value: &str) {
        self.0.insert_attribute(txn, name, value);
    }

    /// Returns a value of an attribute given its `name`. If no attribute with such name existed,
    /// `null` will be returned.
    pub fn get_attribute(&self, txn: &YTransaction, name: &str) -> Option<String> {
        self.0.get_attribute(txn, name)
    }

    /// Removes an attribute from this XML node, given its `name`.
    pub fn remove_attribute(&self, txn: &mut YTransaction, name: &str) {
        self.0.remove_attribute(txn, name);
    }

    /// Returns an iterator that enables to traverse over all attributes of this XML node in
    /// unspecified order.
    pub fn attributes(&self, txn: &YTransaction) -> YXmlAttributes {
        unsafe {
            let this: *const XmlText = &self.0;
            let tx: *const Transaction = txn.deref() as *const _;
            let static_iter: ManuallyDrop<Attributes<'static>> =
                ManuallyDrop::new((*this).attributes(tx.as_ref().unwrap()));
            YXmlAttributes(static_iter)
        }
    }

    /// Subscribes to all operations happening over this instance of `YXmlText`. All changes are
    /// batched and eventually triggered during transaction commit phase.
    /// Returns an `YXmlObserver` which, when free'd, will unsubscribe current callback.
    pub fn observe(&mut self, f: PyObject) -> YXmlTextObserver {
        self.0
            .observe(move |txn, e| {
                Python::with_gil(|py| {
                    let e = YXmlTextEvent::new(e, txn);
                    f.call1(py, (e,)).unwrap();
                })
            })
            .into()
    }
}

#[pyclass(unsendable)]
pub struct YXmlObserver(Subscription<XmlEvent>);

impl From<Subscription<XmlEvent>> for YXmlObserver {
    fn from(o: Subscription<XmlEvent>) -> Self {
        YXmlObserver(o)
    }
}

#[pyclass(unsendable)]
pub struct YXmlTextObserver(Subscription<XmlTextEvent>);

impl From<Subscription<XmlTextEvent>> for YXmlTextObserver {
    fn from(o: Subscription<XmlTextEvent>) -> Self {
        YXmlTextObserver(o)
    }
}

#[pyclass(unsendable)]
pub struct YXmlAttributes(ManuallyDrop<Attributes<'static>>);

impl Drop for YXmlAttributes {
    fn drop(&mut self) {
        unsafe { ManuallyDrop::drop(&mut self.0) }
    }
}

#[pyproto]
impl PyIterProtocol for YXmlAttributes {
    fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }
    fn __next__(mut slf: PyRefMut<Self>) -> Option<(String, String)> {
        slf.0.next().map(|(attr, val)| (attr.to_string(), val))
    }
}

fn xml_into_py(v: Xml) -> PyObject {
    Python::with_gil(|py| match v {
        Xml::Element(v) => YXmlElement(v).into_py(py),
        Xml::Text(v) => YXmlText(v).into_py(py),
    })
}

#[pyclass(unsendable)]
pub struct YXmlTreeWalker(ManuallyDrop<TreeWalker<'static>>);

impl Drop for YXmlTreeWalker {
    fn drop(&mut self) {
        unsafe { ManuallyDrop::drop(&mut self.0) }
    }
}

#[pymethods]
impl YXmlTreeWalker {
    pub fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }
    pub fn __next__(mut slf: PyRefMut<Self>) -> Option<PyObject> {
        Python::with_gil(|py| {
            slf.0.next().map(|v| match v {
                Xml::Element(el) => YXmlElement(el).into_py(py),
                Xml::Text(text) => YXmlText(text).into_py(py),
            })
        })
    }
}

#[pyclass(unsendable)]
pub struct YXmlEvent {
    inner: *const XmlEvent,
    txn: *const Transaction,
    target: Option<PyObject>,
    delta: Option<PyObject>,
    keys: Option<PyObject>,
}
impl YXmlEvent {
    fn new(event: &XmlEvent, txn: &Transaction) -> Self {
        let inner = event as *const XmlEvent;
        let txn = txn as *const Transaction;
        YXmlEvent {
            inner,
            txn,
            target: None,
            delta: None,
            keys: None,
        }
    }

    fn inner(&self) -> &XmlEvent {
        unsafe { self.inner.as_ref().unwrap() }
    }

    fn txn(&self) -> &Transaction {
        unsafe { self.txn.as_ref().unwrap() }
    }
}

#[pymethods]
impl YXmlEvent {
    /// Returns a current shared type instance, that current event changes refer to.
    #[getter]
    pub fn target(&mut self) -> PyObject {
        if let Some(target) = self.target.as_ref() {
            target.clone()
        } else {
            Python::with_gil(|py| {
                let target = YXmlElement(self.inner().target().clone()).into_py(py);
                self.target = Some(target.clone());
                target
            })
        }
    }

    /// Returns an array of keys and indexes creating a path from root type down to current instance
    /// of shared type (accessible via `target` getter).
    /// TODO extract to function
    pub fn path(&self) -> PyObject {
        path_into_py(self.inner().path(self.txn()))
    }

    /// Returns all changes done upon map component of a current shared data type (which can be
    /// accessed via `target`) within a bounds of corresponding transaction `txn`. These
    /// changes are done in result of operations made on `YMap` data type or attribute changes of
    /// `YXmlElement` and `YXmlText` types.
    #[getter]
    pub fn keys(&mut self) -> PyObject {
        if let Some(keys) = &self.keys {
            keys.clone()
        } else {
            Python::with_gil(|py| {
                let keys = self.inner().keys(self.txn());
                let result = PyDict::new(py);
                for (key, value) in keys.iter() {
                    result
                        .set_item(key.deref(), EntryChangeWrapper(value).into_py(py))
                        .unwrap();
                }
                let keys = PyObject::from(result);
                self.keys = Some(keys.clone());
                keys
            })
        }
    }

    /// Returns collection of all changes done over an array component of a current shared data
    /// type (which can be accessed via `target` property). These changes are usually done in result
    /// of operations done on `YArray` and `YText`/`XmlText` types, but also whenever `XmlElement`
    /// children nodes list is modified.
    #[getter]
    pub fn delta(&mut self) -> PyObject {
        if let Some(delta) = &self.delta {
            delta.clone()
        } else {
            Python::with_gil(|py| {
                let delta = self
                    .inner()
                    .delta(self.txn())
                    .into_iter()
                    .map(|v| ChangeWrapper(v).into_py(py));
                let result = pyo3::types::PyList::new(py, delta);
                let delta: PyObject = result.into();
                self.delta = Some(delta.clone());
                delta
            })
        }
    }
}

#[pyclass(unsendable)]
pub struct YXmlTextEvent {
    inner: *const XmlTextEvent,
    txn: *const Transaction,
    target: Option<PyObject>,
    delta: Option<PyObject>,
    keys: Option<PyObject>,
}

impl YXmlTextEvent {
    fn new(event: &XmlTextEvent, txn: &Transaction) -> Self {
        let inner = event as *const XmlTextEvent;
        let txn = txn as *const Transaction;
        YXmlTextEvent {
            inner,
            txn,
            target: None,
            delta: None,
            keys: None,
        }
    }

    fn inner(&self) -> &XmlTextEvent {
        unsafe { self.inner.as_ref().unwrap() }
    }

    fn txn(&self) -> &Transaction {
        unsafe { self.txn.as_ref().unwrap() }
    }
}

#[pymethods]
impl YXmlTextEvent {
    /// Returns a current shared type instance, that current event changes refer to.
    #[getter]
    pub fn target(&mut self) -> PyObject {
        if let Some(target) = self.target.as_ref() {
            target.clone()
        } else {
            Python::with_gil(|py| {
                let target = YXmlText(self.inner().target().clone()).into_py(py);
                self.target = Some(target.clone());
                target
            })
        }
    }

    /// Returns a current shared type instance, that current event changes refer to.
    pub fn path(&self) -> PyObject {
        path_into_py(self.inner().path(self.txn()))
    }

    /// Returns all changes done upon map component of a current shared data type (which can be
    /// accessed via `target`) within a bounds of corresponding transaction `txn`. These
    /// changes are done in result of operations made on `YMap` data type or attribute changes of
    /// `YXmlElement` and `YXmlText` types.
    #[getter]
    pub fn keys(&mut self) -> PyObject {
        if let Some(keys) = &self.keys {
            keys.clone()
        } else {
            Python::with_gil(|py| {
                let keys = self.inner().keys(self.txn());
                let result = PyDict::new(py);
                for (key, value) in keys.iter() {
                    result
                        .set_item(key.deref(), EntryChangeWrapper(value).into_py(py))
                        .unwrap();
                }
                let keys = PyObject::from(result);
                self.keys = Some(keys.clone());
                keys
            })
        }
    }

    /// Returns a list of text changes made over corresponding `YXmlText` collection within
    /// bounds of current transaction. These changes follow a format:
    ///
    /// - { insert: string, attributes: any|undefined }
    /// - { delete: number }
    /// - { retain: number, attributes: any|undefined }
    #[getter]
    pub fn delta(&mut self) -> PyObject {
        if let Some(delta) = &self.delta {
            delta.clone()
        } else {
            Python::with_gil(|py| {
                let delta = self
                    .inner()
                    .delta(self.txn())
                    .into_iter()
                    .map(ytext_delta_into_py);
                let result = pyo3::types::PyList::new(py, delta);
                let delta: PyObject = result.into();
                self.delta = Some(delta.clone());
                delta
            })
        }
    }
}

/// Converts a Y.rs Path object into a Python object.
fn path_into_py(path: Path) -> PyObject {
    Python::with_gil(|py| {
        let result = PyList::empty(py);
        for segment in path {
            match segment {
                PathSegment::Key(key) => {
                    result.append(key.as_ref()).unwrap();
                }
                PathSegment::Index(idx) => {
                    result.append(idx).unwrap();
                }
            }
        }
        result.into()
    })
}

fn ytext_delta_into_py(delta: &Delta) -> PyObject {
    Python::with_gil(|py| {
        let result = PyDict::new(py);
        match delta {
            Delta::Inserted(value, attrs) => {
                let value = ValueWrapper(value.clone()).into_py(py);
                result.set_item("insert", value).unwrap();

                if let Some(attrs) = attrs {
                    let attrs = attrs_into_py(attrs);
                    result.set_item("attributes", attrs).unwrap();
                }
            }
            Delta::Retain(len, attrs) => {
                result.set_item("retain", len).unwrap();

                if let Some(attrs) = attrs {
                    let attrs = attrs_into_py(attrs);
                    result.set_item("attributes", attrs).unwrap();
                }
            }
            Delta::Deleted(len) => {
                result.set_item("delete", len).unwrap();
            }
        }
        result.into()
    })
}

fn attrs_into_py(attrs: &Attrs) -> PyObject {
    Python::with_gil(|py| {
        let o = PyDict::new(py);
        for (key, value) in attrs.iter() {
            let key = key.as_ref();
            let value = ValueWrapper(Value::Any(value.clone())).into_py(py);
            o.set_item(key, value).unwrap();
        }
        o.into()
    })
}

struct ChangeWrapper<'a>(&'a Change);

impl<'a> IntoPy<PyObject> for ChangeWrapper<'a> {
    fn into_py(self, py: Python) -> PyObject {
        let result = PyDict::new(py);
        match self.0 {
            Change::Added(values) => {
                let values: Vec<PyObject> = values
                    .into_iter()
                    .map(|v| ValueWrapper(v.clone()).into_py(py))
                    .collect();
                result.set_item("insert", values).unwrap();
            }
            Change::Removed(len) => {
                result.set_item("delete", len).unwrap();
            }
            Change::Retain(len) => {
                result.set_item("retain", len).unwrap();
            }
        }
        result.into()
    }
}

struct EntryChangeWrapper<'a>(&'a EntryChange);

impl<'a> IntoPy<PyObject> for EntryChangeWrapper<'a> {
    fn into_py(self, py: Python) -> PyObject {
        let result = PyDict::new(py);
        let action = "action";
        match self.0 {
            EntryChange::Inserted(new) => {
                let new_value = ValueWrapper(new.clone()).into_py(py);
                result.set_item(action, "add").unwrap();
                result.set_item("newValue", new_value).unwrap();
            }
            EntryChange::Updated(old, new) => {
                let old_value = ValueWrapper(old.clone()).into_py(py);
                let new_value = ValueWrapper(new.clone()).into_py(py);
                result.set_item(action, "update").unwrap();
                result.set_item("oldValue", old_value).unwrap();
                result.set_item("newValue", new_value).unwrap();
            }
            EntryChange::Removed(old) => {
                let old_value = ValueWrapper(old.clone()).into_py(py);
                result.set_item(action, "delete").unwrap();
                result.set_item("oldValue", old_value).unwrap();
            }
        }
        result.into()
    }
}

struct PyObjectWrapper(PyObject);

impl Prelim for PyObjectWrapper {
    fn into_content(self, _txn: &mut Transaction, ptr: TypePtr) -> (ItemContent, Option<Self>) {
        let guard = Python::acquire_gil();
        let py = guard.python();
        let content = if let Some(any) = py_into_any(self.0.clone()) {
            ItemContent::Any(vec![any])
        } else if let Ok(shared) = Shared::extract(self.0.as_ref(py)) {
            if shared.is_prelim() {
                let branch = BranchRef::new(Branch::new(ptr, shared.type_ref(), None));
                ItemContent::Type(branch)
            } else {
                panic!("Cannot integrate this type")
            }
        } else {
            panic!("Cannot integrate this type")
        };

        let this = if let ItemContent::Type(_) = &content {
            Some(self)
        } else {
            None
        };

        (content, this)
    }

    fn integrate(self, txn: &mut Transaction, inner_ref: BranchRef) {
        let guard = Python::acquire_gil();
        let py = guard.python();
        let obj_ref = self.0.as_ref(py);
        if let Ok(shared) = Shared::extract(obj_ref) {
            if shared.is_prelim() {
                Python::with_gil(|py| match shared {
                    Shared::Text(v) => {
                        let text = Text::from(inner_ref);
                        let mut y_text = v.borrow_mut(py);

                        if let SharedType::Prelim(v) = y_text.0.to_owned() {
                            text.push(txn, v.as_str());
                        }
                        y_text.0 = SharedType::Integrated(text.clone());
                    }
                    Shared::Array(v) => {
                        let array = Array::from(inner_ref);
                        let mut y_array = v.borrow_mut(py);
                        if let SharedType::Prelim(items) = y_array.0.to_owned() {
                            let len = array.len();
                            insert_at(&array, txn, len, items);
                        }
                        y_array.0 = SharedType::Integrated(array.clone());
                    }
                    Shared::Map(v) => {
                        let map = Map::from(inner_ref);
                        let mut y_map = v.borrow_mut(py);
                        if let SharedType::Prelim(entries) = y_map.0.to_owned() {
                            for (k, v) in entries {
                                map.insert(txn, k, PyValueWrapper(v));
                            }
                        }
                        y_map.0 = SharedType::Integrated(map.clone());
                    }
                    _ => panic!("Cannot integrate this type"),
                })
            }
        }
    }
}

fn insert_at(dst: &Array, txn: &mut Transaction, index: u32, src: Vec<PyObject>) {
    let mut j = index;
    let mut i = 0;
    while i < src.len() {
        let mut anys = Vec::default();
        while i < src.len() {
            if let Some(any) = py_into_any(src[i].clone()) {
                anys.push(any);
                i += 1;
            } else {
                break;
            }
        }

        if !anys.is_empty() {
            let len = anys.len() as u32;
            dst.insert_range(txn, j, anys);
            j += len;
        } else {
            let wrapper = PyObjectWrapper(src[i].clone());
            dst.insert(txn, j, wrapper);
            i += 1;
            j += 1;
        }
    }
}

fn py_into_any(v: PyObject) -> Option<Any> {
    Python::with_gil(|py| -> Option<Any> {
        let v = v.as_ref(py);

        if let Ok(s) = v.downcast::<pytypes::PyString>() {
            let string: String = s.extract().unwrap();
            Some(Any::String(string.into_boxed_str()))
        } else if let Ok(l) = v.downcast::<pytypes::PyLong>() {
            let i: f64 = l.extract().unwrap();
            Some(Any::BigInt(i as i64))
        } else if v == py.None().as_ref(py) {
            Some(Any::Null)
        } else if let Ok(f) = v.downcast::<pytypes::PyFloat>() {
            Some(Any::Number(f.extract().unwrap()))
        } else if let Ok(b) = v.downcast::<pytypes::PyBool>() {
            Some(Any::Bool(b.extract().unwrap()))
        } else if let Ok(list) = v.downcast::<pytypes::PyList>() {
            let mut result = Vec::with_capacity(list.len());
            for value in list.iter() {
                result.push(py_into_any(value.into())?);
            }
            Some(Any::Array(result.into_boxed_slice()))
        } else if let Ok(dict) = v.downcast::<pytypes::PyDict>() {
            if let Ok(_) = Shared::extract(v) {
                None
            } else {
                let mut result = HashMap::new();
                for (k, v) in dict.iter() {
                    let key = k
                        .downcast::<pytypes::PyString>()
                        .unwrap()
                        .extract()
                        .unwrap();
                    let value = py_into_any(v.into())?;
                    result.insert(key, value);
                }
                Some(Any::Map(Box::new(result)))
            }
        } else {
            None
        }
    })
}

pub struct XmlWrapper(Xml);

impl IntoPy<PyObject> for XmlWrapper {
    fn into_py(self, py: Python) -> PyObject {
        match self.0 {
            Xml::Element(v) => YXmlElement(v).into_py(py),
            Xml::Text(v) => YXmlText(v).into_py(py),
        }
    }
}

pub struct AnyWrapper(Any);

impl IntoPy<pyo3::PyObject> for AnyWrapper {
    fn into_py(self, py: Python) -> pyo3::PyObject {
        match self.0 {
            Any::Null | Any::Undefined => py.None(),
            Any::Bool(v) => v.into_py(py),
            Any::Number(v) => v.into_py(py),
            Any::BigInt(v) => v.into_py(py),
            Any::String(v) => v.into_py(py),
            Any::Buffer(v) => {
                let byte_array = PyByteArray::new(py, v.as_ref());
                byte_array.into()
            }
            Any::Array(v) => {
                let mut a = Vec::new();
                for value in v.iter() {
                    let value = AnyWrapper(value.to_owned());
                    a.push(value);
                }
                a.into_py(py)
            }
            Any::Map(v) => {
                let mut m = HashMap::new();
                for (k, v) in v.iter() {
                    let value = AnyWrapper(v.to_owned());
                    m.insert(k, value);
                }
                m.into_py(py)
            }
        }
    }
}

impl Deref for AnyWrapper {
    type Target = Any;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

pub struct ValueWrapper(Value);

impl IntoPy<pyo3::PyObject> for ValueWrapper {
    fn into_py(self, py: Python) -> pyo3::PyObject {
        match self.0 {
            Value::Any(v) => AnyWrapper(v).into_py(py),
            Value::YText(v) => YText::from(v).into_py(py),
            Value::YArray(v) => YArray::from(v).into_py(py),
            Value::YMap(v) => YMap::from(v).into_py(py),
            Value::YXmlElement(v) => YXmlElement(v).into_py(py),
            Value::YXmlText(v) => YXmlText(v).into_py(py),
        }
    }
}

struct PyValueWrapper(PyObject);

impl Prelim for PyValueWrapper {
    fn into_content(self, _txn: &mut Transaction, ptr: TypePtr) -> (ItemContent, Option<Self>) {
        let content = if let Some(any) = py_into_any(self.0.clone()) {
            ItemContent::Any(vec![any])
        } else if let Ok(shared) = Shared::try_from(self.0.clone()) {
            if shared.is_prelim() {
                let branch = BranchRef::new(Branch::new(ptr, shared.type_ref(), None));
                ItemContent::Type(branch)
            } else {
                panic!("Cannot integrate this type")
            }
        } else {
            panic!("Cannot integrate this type")
        };

        let this = if let ItemContent::Type(_) = &content {
            Some(self)
        } else {
            None
        };

        (content, this)
    }

    fn integrate(self, txn: &mut Transaction, inner_ref: BranchRef) {
        if let Ok(shared) = Shared::try_from(self.0) {
            if shared.is_prelim() {
                Python::with_gil(|py| match shared {
                    Shared::Text(v) => {
                        let text = Text::from(inner_ref);
                        let mut y_text = v.borrow_mut(py);

                        if let SharedType::Prelim(v) = y_text.0.to_owned() {
                            text.push(txn, v.as_str());
                        }
                        y_text.0 = SharedType::Integrated(text.clone());
                    }
                    Shared::Array(v) => {
                        let array = Array::from(inner_ref);
                        let mut y_array = v.borrow_mut(py);
                        if let SharedType::Prelim(items) = y_array.0.to_owned() {
                            let len = array.len();
                            insert_at(&array, txn, len, items);
                        }
                        y_array.0 = SharedType::Integrated(array.clone());
                    }
                    Shared::Map(v) => {
                        let map = Map::from(inner_ref);
                        let mut y_map = v.borrow_mut(py);

                        if let SharedType::Prelim(entries) = y_map.0.to_owned() {
                            for (k, v) in entries {
                                map.insert(txn, k, PyValueWrapper(v));
                            }
                        }
                        y_map.0 = SharedType::Integrated(map.clone());
                    }
                    _ => panic!("Cannot integrate this type"),
                })
            }
        }
    }
}

#[derive(FromPyObject)]
enum Shared {
    Text(Py<YText>),
    Array(Py<YArray>),
    Map(Py<YMap>),
    XmlElement(Py<YXmlElement>),
    XmlText(Py<YXmlText>),
}

impl Shared {
    fn is_prelim(&self) -> bool {
        Python::with_gil(|py| match self {
            Shared::Text(v) => v.borrow(py).prelim(),
            Shared::Array(v) => v.borrow(py).prelim(),
            Shared::Map(v) => v.borrow(py).prelim(),
            Shared::XmlElement(_) | Shared::XmlText(_) => false,
        })
    }

    fn type_ref(&self) -> TypeRefs {
        match self {
            Shared::Text(_) => TYPE_REFS_TEXT,
            Shared::Array(_) => TYPE_REFS_ARRAY,
            Shared::Map(_) => TYPE_REFS_MAP,
            Shared::XmlElement(_) => TYPE_REFS_XML_ELEMENT,
            Shared::XmlText(_) => TYPE_REFS_XML_TEXT,
        }
    }
}

impl TryFrom<PyObject> for Shared {
    type Error = PyErr;

    fn try_from(value: PyObject) -> Result<Self, Self::Error> {
        Python::with_gil(|py| {
            let value = value.as_ref(py);

            if let Ok(text) = value.extract() {
                Ok(Shared::Text(text))
            } else if let Ok(array) = value.extract() {
                Ok(Shared::Array(array))
            } else if let Ok(map) = value.extract() {
                Ok(Shared::Map(map))
            } else {
                Err(pyo3::exceptions::PyValueError::new_err(
                    "Could not extract Python value into a shared type.",
                ))
            }
        })
    }
}

/// Python bindings for Y.rs
#[pymodule]
pub fn y_py(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<YDoc>()?;
    m.add_class::<YText>()?;
    m.add_class::<YArray>()?;
    m.add_class::<YArrayIterator>()?;
    m.add_class::<YMap>()?;
    m.add_class::<YMapIterator>()?;
    m.add_class::<YXmlText>()?;
    m.add_class::<YXmlElement>()?;
    m.add_wrapped(wrap_pyfunction!(encode_state_vector))?;
    m.add_wrapped(wrap_pyfunction!(encode_state_as_update))?;
    m.add_wrapped(wrap_pyfunction!(apply_update))?;
    Ok(())
}
