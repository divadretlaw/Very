//
//  Clean.swift
//  very
//
//  Created by David Walter on 05.07.20.
//

import Foundation
import SwiftCLI

extension Very {
    class Clean: Command {
        let name = "clean"
        let shortDescription = "Cleans the system"
        
        @Flag("-a", "--additional", description: "Runs additional clean commands.")
        var additional: Bool
        
        @Flag("-d", "--directories", description: "Removes contents of directories.")
        var directories: Bool
        
        @Flag("-t", "--trash", description: "Empties the trash.")
        var trash: Bool
        
        @Flag("--wow", description: "Runs all clean commands.")
        var wow: Bool
        
        func execute() throws {
            let freeSpaceBefore = DiskCommands.getFreeSpace()
            
            if wow {
                CleanCommands.all()
            } else if anyFlag {
                CleanCommands.default()
                if trash {
                    CleanCommands.trash()
                }
                
                if additional {
                    CleanCommands.additional()
                }
                
                if directories {
                    CleanCommands.directories()
                }
            } else {
                CleanCommands.default()
            }
            
            guard let bytes = DiskCommands.getFreeSpace(relativeTo: freeSpaceBefore) else {
                Log.done()
                return
            }
            
            let formatter = ByteCountFormatter()
            formatter.countStyle = .file
            Log.done("\(formatter.string(fromByteCount: Int64(bytes)).cyan) of space was saved.")
        }
        
        var anyFlag: Bool {
            return additional || directories || trash || wow
        }
    }
}
