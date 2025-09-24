use nix::{libc, unistd::fork};

fn main() {
    unsafe {fork().unwrap();};
    println!("getpid: {}, getppid: {}", unsafe {libc::getpid()}, unsafe {libc::getppid()});
}
