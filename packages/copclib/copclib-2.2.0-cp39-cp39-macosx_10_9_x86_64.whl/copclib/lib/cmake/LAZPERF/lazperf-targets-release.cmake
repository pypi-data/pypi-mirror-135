#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "LAZPERF::lazperf" for configuration "Release"
set_property(TARGET LAZPERF::lazperf APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(LAZPERF::lazperf PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/liblazperf.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/liblazperf.dylib"
  )

list(APPEND _IMPORT_CHECK_TARGETS LAZPERF::lazperf )
list(APPEND _IMPORT_CHECK_FILES_FOR_LAZPERF::lazperf "${_IMPORT_PREFIX}/lib/liblazperf.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
