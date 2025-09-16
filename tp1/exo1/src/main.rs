use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        panic!("Usage: {} <name>", args[0]);
    }
    // Check for the "-g" flag : la façon simple
    // let option_g = args.contains("-g")
    let mut option_g = false;
    for i in 0..args.len() {
        if args[i] == "-g" {
            option_g = true;
        }
    }
    if option_g { 
        dbg!(&args);
        // println!("{:?}", &args);
    }
    for arg in &args[1..] {
        if arg != "-g" {
            println!("Bonjour, {}!", arg);
        }
    }
}

// fn main() {
//     println!("Hello, world!");
// }
