use nix::sys::wait::wait;
use nix::sys::wait::WaitStatus;
use nix::unistd::fork;
use nix::unistd::ForkResult;
use nix::unistd::write;
use nix::libc;
//use nix::{sys::wait::waitpid,unistd::{fork, ForkResult, write}};



fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut x = 0;
    let fork_result = unsafe { fork()? };
    if let ForkResult::Parent { child, .. } = fork_result {
        println!("Continuing execution in parent process, new child has pid: {}", child);
        let wait_status: nix::sys::wait::WaitStatus = wait()?;
        if let WaitStatus::Exited(pid_du_fils, code_sortie) = wait_status {
            println!("[père] le fils {} a terminé avec le code de sortie {}, x = {}", pid_du_fils, code_sortie, x);
        }
    } else {
        // Unsafe to use `println!` (or `unwrap`) here. See Safety.
        x = 1;
        write(std::io::stdout(), format!("I'm a new child process, x = {}\n", x).as_bytes()).ok();
        unsafe { libc::_exit(42) };
    }
    Ok(())
}
