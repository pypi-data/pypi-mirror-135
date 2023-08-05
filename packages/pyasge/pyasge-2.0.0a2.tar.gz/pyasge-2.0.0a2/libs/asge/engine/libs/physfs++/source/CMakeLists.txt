set(PHYSFSCPP_VERSION 0.1.0)
set(PHYSFSCPP_SOVERSION 1)

# Don't use -rpath.
if(CMAKE_COMPILER_IS_GNUCC)
    set(CMAKE_SKIP_RPATH ON CACHE BOOL "Skip RPATH" FORCE)
endif()

option(PHYSFS_BUILD_STATIC "Build static library" TRUE)
if(PHYSFS_BUILD_STATIC)
    # static libraries use a different target
    set(PHYSFS_LIB_TARGET physfscpp-static )
    add_library(${PHYSFS_LIB_TARGET} STATIC PhysFS/PhysFS.cpp ${PHYSFSCPP_HEADERS})
    target_compile_definitions(${PHYSFS_LIB_TARGET} PRIVATE PHYSFS_CPP_STATIC)
    if(NOT MSVC)
        set_target_properties(${PHYSFS_LIB_TARGET} PROPERTIES OUTPUT_NAME "physfscpp")
    endif()

    # where to store all these lovely build artefacts
    set(PHYSFS_INSTALL_TARGETS ${PHYSFS_INSTALL_TARGETS} ";${PHYSFS_LIB_TARGET}")

    # assume we want to ink against the static version of physfs
    target_link_libraries(${PHYSFS_LIB_TARGET} PUBLIC physfs-static)
endif()

option(PHYSFS_BUILD_SHARED "Build shared library" FALSE)
if(PHYSFS_BUILD_SHARED)
    set(PHYSFS_LIB_TARGET physfscpp )
    add_library(${PHYSFS_LIB_TARGET} SHARED PhysFS/PhysFS.cpp ${PHYSFSCPP_HEADERS})
    target_compile_definitions(${PHYSFS_LIB_TARGET} PRIVATE PHYSFS_CPP_EXPORT)
    set_target_properties(${PHYSFS_LIB_TARGET} PROPERTIES MACOSX_RPATH 1)
    set_target_properties(${PHYSFS_LIB_TARGET} PROPERTIES VERSION ${PHYSFSCPP_VERSION})
    set_target_properties(${PHYSFS_LIB_TARGET} PROPERTIES SOVERSION ${PHYSFSCPP_SOVERSION})

    # where to store all these lovely build artefacts
    set(PHYSFS_INSTALL_TARGETS ${PHYSFS_INSTALL_TARGETS} ";physfscpp")

    # assume we want to ink against the shared version of physfs
    target_link_libraries(${PHYSFS_LIB_TARGET} PUBLIC physfs)
endif()


if(NOT PHYSFS_BUILD_SHARED AND NOT PHYSFS_BUILD_STATIC)
    message(FATAL "Both shared and static libraries are disabled!")
endif()

target_include_directories(
        ${PHYSFS_LIB_TARGET}
        PUBLIC
        "$<BUILD_INTERFACE:${PHYSFSCPP_HEADER_DIR}>"
        "${PHYSFS_HEADER_DIR}"
)

if(PHYSFS_BUILD_SHARED AND PHYSFS_BUILD_STATIC AND NOT WINDOWS)
    set_target_properties(physfscpp PROPERTIES CLEAN_DIRECT_OUTPUT 1)
    set_target_properties(physfscpp-static PROPERTIES CLEAN_DIRECT_OUTPUT 1)
endif()

install(TARGETS ${PHYSFS_INSTALL_TARGETS}
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib${LIB_SUFFIX}
        ARCHIVE DESTINATION lib${LIB_SUFFIX})
install(FILES "${PHYSFSCPP_HEADERS}" DESTINATION include)

macro(message_bool_option _NAME _VALUE)
    if(${_VALUE})
        message(STATUS "  ${_NAME}: enabled")
    else()
        message(STATUS "  ${_NAME}: disabled")
    endif()
endmacro()

message(STATUS "PhysicsFS++ will build with the following options:")
message_bool_option("Build static library" PHYSFS_BUILD_STATIC)
message_bool_option("Build shared library" PHYSFS_BUILD_SHARED)