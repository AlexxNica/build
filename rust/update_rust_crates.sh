#!/bin/bash

cargo vendor --sync $FUCHSIA_ROOT/garnet/Cargo.toml $FUCHSIA_ROOT/third_party/rust-crates/vendor
python $FUCHSIA_ROOT/scripts/rust/check_rust_licenses.py --directory third_party/rust-crates/vendor --verify
