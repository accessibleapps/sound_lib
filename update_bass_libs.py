#!/usr/bin/env python3
"""Bass library updater command-line interface."""
import argparse
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from bass_updater.updater import BassUpdater
from bass_updater.config import BASS_LIBRARIES


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Update Bass audio libraries from un4seen.com"
    )
    
    parser.add_argument(
        '--check', '-c',
        action='store_true',
        help='Check for updates without installing'
    )
    
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true', 
        help='Show what would be updated without making changes'
    )
    
    parser.add_argument(
        '--library', '-l',
        choices=list(BASS_LIBRARIES.keys()),
        help='Update only the specified library'
    )
    
    parser.add_argument(
        '--list-libraries',
        action='store_true',
        help='List all supported libraries'
    )
    
    parser.add_argument(
        '--platforms', '-p',
        nargs='+',
        choices=['win32', 'win64', 'linux', 'macos'],
        help='Limit updates to specified platforms'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    if args.list_libraries:
        print("Supported Bass libraries:")
        for lib_key, (display_name, _, _) in BASS_LIBRARIES.items():
            print(f"  {lib_key:<12} - {display_name}")
        return 0
        
    try:
        updater = BassUpdater()
        
        if args.check:
            updates = updater.check_for_updates()
            if updates:
                print(f"\n{len(updates)} libraries have updates available.")
                return 1  # Exit code indicates updates available
            else:
                print("\nAll libraries are up to date.")
                return 0
                
        elif args.library:
            # Update single library
            updates = updater.check_for_updates()
            if args.library not in updates:
                print(f"{args.library} is already up to date.")
                return 0
                
            old_version, new_version = updates[args.library]
            
            if args.dry_run:
                print(f"Would update {args.library}: {old_version or 'not installed'} → {new_version}")
                return 0
                
            success = updater.update_library(args.library, new_version, args.platforms)
            return 0 if success else 1
            
        else:
            # Update all libraries
            results = updater.update_all(dry_run=args.dry_run)
            
            if not results:
                print("No updates available.")
                return 0
                
            if args.dry_run:
                return 0
                
            # Report results
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            if successful == total:
                print(f"\nSuccessfully updated all {total} libraries.")
                return 0
            else:
                failed = total - successful
                print(f"\nUpdated {successful}/{total} libraries. {failed} failed.")
                return 1
                
    except KeyboardInterrupt:
        print("\nUpdate cancelled by user.")
        return 130
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1
    finally:
        try:
            updater.cleanup()
        except:
            pass


if __name__ == '__main__':
    sys.exit(main())