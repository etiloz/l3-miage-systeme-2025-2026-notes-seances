use nix::unistd::fork;
use nix::unistd::sleep;

fn main() {
    let fork_result =  unsafe {fork().expect("Failed to fork")};
    match fork_result {
        nix::unistd::ForkResult::Parent { child } => {
            println!("le père commence à attendre");
            let _ = nix::sys::wait::waitpid(child, None).expect("Failed to wait on child");
            println!("le fils a terminé");
        }
        nix::unistd::ForkResult::Child => {
            sleep(10);
            println!("bye");
        }

    }
}
