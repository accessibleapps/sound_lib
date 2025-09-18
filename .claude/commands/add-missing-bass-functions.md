---
description: Add missing BASS functions to sound_lib with pythonic wrappers
allowed-tools: Bash, Read, Write, Edit, MultiEdit, Grep, Glob, TodoWrite, mcp__sequentialthinking__sequentialthinking
---

# Add Missing BASS Functions to sound_lib

## Context Gathering
!`ls markdown/BASS_*.md | wc -l`
!`grep -c "^BASS_Channel" sound_lib/external/pybass.py`
!`git status --porcelain`

## Your Task
Systematically discover and add missing BASS functions to sound_lib by comparing documentation to implementation, then create pythonic wrapper methods. Focus on $ARGUMENTS if provided (e.g., "BASS_Channel", "BASS_Stream"), otherwise analyze all BASS functions.

### Phase 1: Gap Analysis
1. **Scan documentation**: Use Glob to find all relevant markdown files in `markdown/` directory
2. **Extract function signatures**: Read each doc file to identify BASS function signatures and parameters
3. **Check existing implementation**: Grep through `sound_lib/external/pybass.py` to find what's already implemented
4. **Identify gaps**: Create list of missing functions, noting their signatures and purpose
5. **Prioritize functions**: Focus on functions that would provide significant value to sound_lib users

### Phase 2: Low-Level Integration Planning
1. **Analyze function signatures**: Determine proper ctypes declarations for each missing function
2. **Identify required constants**: Check if new BASS_* constants need to be added
3. **Plan placement**: Determine where in pybass.py each function should be added (group with related functions)
4. **Design validation**: Plan how to verify each function works correctly

### Phase 3: Implementation - Low-Level Bindings
For each missing function:
1. **Add constants first**: If function requires new BASS_* constants, add them to pybass.py in appropriate section
2. **Add function declaration**: Add properly formatted ctypes function declaration with:
   - Commented C signature for reference
   - Correct parameter types (c_ulong, POINTER, etc.)
   - Correct return type
   - Proper function name mapping
3. **Commit atomically**: Make single commit per function addition with descriptive message
4. **Test basic binding**: Verify the function can be imported without errors

### Phase 4: High-Level Wrapper Design
1. **Identify target class**: Determine which class should receive the wrapper method (Channel, Stream, etc.)
2. **Design pythonic interface**: Plan method signature with:
   - Sensible parameter defaults
   - Python-native return types (lists instead of arrays, None instead of null pointers)
   - Automatic memory management (no manual buffer allocation)
   - Clear parameter names (not just BASS constant names)
3. **Plan convenience methods**: Identify common use cases that deserve simplified wrapper methods
4. **Follow existing patterns**: Ensure consistency with existing sound_lib method patterns

### Phase 5: Implementation - High-Level Wrappers
For each function:
1. **Add primary wrapper method**: Implement main wrapper with:
   - Comprehensive docstring with Args/Returns/Raises sections
   - Proper error handling using bass_call/bass_call_0
   - Pythonic parameter handling and type conversion
   - Memory management for buffers and arrays
2. **Add convenience methods**: Create simplified methods for common use cases
3. **Test integration**: Verify method works with existing Channel/Stream patterns
4. **Commit atomically**: Single commit per method addition

### Phase 6: Verification and Documentation
1. **Code review**: Ensure all new methods follow sound_lib conventions
2. **Error handling verification**: Test that BassError is properly raised
3. **Memory management check**: Verify no memory leaks in buffer handling
4. **Integration testing**: Test new methods work with existing sound_lib functionality
5. **Update imports if needed**: Add any missing imports to channel.py or other files

## Success Criteria
- All missing functions identified through systematic documentation analysis
- Each function added to pybass.py with proper ctypes declaration
- Each function committed atomically with clear commit message
- High-level wrapper methods added with pythonic interfaces
- All methods follow existing sound_lib patterns and conventions
- Proper error handling and memory management implemented
- Documentation includes clear docstrings with type information
- No regressions in existing functionality
- Each wrapper method committed atomically

## Implementation Notes
- **Atomic commits required**: Each function/method addition must be committed separately per Q's requirements
- **Pythonic design**: Convert BASS C patterns to proper Python idioms (lists, None, automatic memory management)
- **Follow patterns**: Study existing Channel class methods to maintain consistency
- **Documentation-driven**: Use markdown docs as authoritative source for function signatures
- **Error handling**: Use existing bass_call/bass_call_0 patterns for proper BassError integration
- **Memory safety**: Handle ctypes buffers and arrays safely with automatic cleanup

## Quality Checks
- Does each wrapper hide ctypes complexity from end users?
- Are return types properly converted to Python natives?
- Do parameter names clearly indicate their purpose?
- Is memory management automatic (no manual allocation required)?
- Do convenience methods cover common use cases simply?
- Are all commits atomic and descriptive?
- Does error handling follow existing patterns?