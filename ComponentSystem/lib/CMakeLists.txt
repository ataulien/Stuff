# Generates a list of all subdirs from the given one


# Build BGFX
include_directories(bx/include)

# include all 3rd-party dirs
SET(BGFX_3RDPARTYINC bgfx/3rdparty/khronos
                bgfx/3rdparty/dxsdk
                bgfx/3rdparty/edtaa3
                bgfx/3rdparty/etc1
                bgfx/3rdparty/etc2
                bgfx/3rdparty/fcpp
                bgfx/3rdparty/forsyth-too
                bgfx/3rdparty/freetype
                bgfx/3rdparty/glsl-optimizer
                bgfx/3rdparty/ib-compress
                bgfx/3rdparty/edtaa3
                bgfx/3rdparty/libsquish
                bgfx/3rdparty/renderdoc
                bgfx/3rdparty/scintilla
                bgfx/3rdparty/openvr
                bgfx/3rdparty/ocornut-imgui
                bgfx/3rdparty
        )
include_directories(${BGFX_3RDPARTYINC})

find_package(OpenGL REQUIRED)
add_library(bgfx STATIC bgfx/src/amalgamated.cpp)
target_link_libraries(bgfx ${OPENGL_LIBRARIES} dl X11 pthread)

foreach(d ${BGFX_3RDPARTYINC})
    SET(BGFX_3RDPARTY_SRC_FILES "${BGFX_3RDPARTY_SRC_FILES} ${d}/*.h")
    SET(BGFX_3RDPARTY_SRC_FILES "${BGFX_3RDPARTY_SRC_FILES} ${d}/*.cpp")
endforeach()

set( BGFX_3RDPARTY_SRC_FILES ${BGFX_3RDPARTY_SRC_FILES} )
separate_arguments(BGFX_3RDPARTY_SRC_FILES)


file(GLOB COMMON_SRC
        bgfx/examples/common/*.h
        bgfx/examples/common/*.cpp
        bgfx/examples/common/entry/*.h
        bgfx/examples/common/entry/*.cpp
        bgfx/examples/common/debugdraw/*.h
        bgfx/examples/common/debugdraw/*.cpp
        bgfx/examples/common/font/*.h
        bgfx/examples/common/font/*.cpp
        bgfx/examples/common/imgui/*.h
        bgfx/examples/common/imgui/*.cpp
        bgfx/examples/common/nanovg/*.h
        bgfx/examples/common/nanovg/*.cpp
        ${BGFX_3RDPARTY_SRC_FILES})

add_library(bgfx_common STATIC ${COMMON_SRC})