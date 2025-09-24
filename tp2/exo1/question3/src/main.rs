use nix::unistd::fork;
use nix::unistd::sleep;

fn main() {
    unsafe {fork().unwrap();};
    sleep(10);
    println!("bye");
}
