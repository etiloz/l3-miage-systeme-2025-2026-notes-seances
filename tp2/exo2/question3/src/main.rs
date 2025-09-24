use nix::unistd::fork;
use nix::unistd::sleep;
use nix::sys::wait::waitpid;
use nix::sys::wait::WaitStatus;
use nix::unistd::ForkResult;
use rand;

fn main() {
    let fork_result =  unsafe {fork().expect("Failed to fork")};
    match fork_result {
        ForkResult::Parent { child } => {
            println!("le père commence à attendre");
            let wait_status = waitpid(child, None).expect("Failed to wait on child");
            match wait_status {
                WaitStatus::Exited(_pid_du_fils, code_de_sortie) => {
                    println!("Le fils s'est terminé avec le code de sortie : {}", code_de_sortie);
                }
                WaitStatus::Signaled(_pid_du_fils, signal, _) => {
                    println!("Le fils a été tué par le signal : {:?}", signal);
                }
                _ => {
                    println!("Le fils a changé d'état (sans terminer vraiment) : {:?}", wait_status);
                }
            }
        }
        ForkResult::Child => {
            sleep(10);
            let code_de_sortie: i32 = rand::random::<i32>() % 10; // Code de sortie aléatoire entre 0 et 10
            println!("Le fils se termine avec le code de sortie : {}", code_de_sortie);
            println!("bye");
            unsafe { nix::libc::exit(code_de_sortie); }
        }

    }
}
