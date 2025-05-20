use std::str::from_utf8;

fn variation_selector_to_byte(variation_selector: char) -> Option<u8> {
    let variation_selector = variation_selector as u32;
    if (0xFE00..=0xFE0F).contains(&variation_selector) {
        Some((variation_selector - 0xFE00) as u8)
    } else if (0xE0100..=0xE01EF).contains(&variation_selector) {
        Some((variation_selector - 0xE0100 + 16) as u8)
    } else {
        None
    }
}

fn decode(emoji_string: &str) -> Vec<u8> {
    let mut result = Vec::new();
    let mut current_bytes = Vec::new();
    
    for emoji in emoji_string.chars() {
        if let Some(byte) = variation_selector_to_byte(emoji) {
            current_bytes.push(byte);
        } else {
            if !current_bytes.is_empty() {
                result.append(&mut current_bytes);
            }
        }
    }
    
    if !current_bytes.is_empty() {
        result.append(&mut current_bytes);
    }
    
    result.retain(|&b| b.is_ascii()); 
    result
}

fn main() {
    let encoded_flag = "😀󠄷󠄿󠄳󠅄󠄶󠅫🥰󠅓󠅢󠅩󠅠󠅤󠄠󠅏🌙󠄣󠅝󠅟󠅚󠄡󠅏💯󠅕󠅦󠅙󠄡󠅭"; 
    let decoded_bytes = decode(encoded_flag);
    println!("Decoded bytes: {:?}", decoded_bytes);
    
    match from_utf8(&decoded_bytes) {
        Ok(flag) => println!("Decoded flag: {}", flag),
        Err(e) => println!("Failed to decode UTF-8: {:?}", e),
    }
}


