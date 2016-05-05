cmake_minimum_required(VERSION 2.4)
project(ComponentSystem)

set(CMAKE_CXX_STANDARD 14)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Ofast -O3 -s")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -flto")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -ffast-math")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fomit-frame-pointer")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fno-math-errno")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -funsafe-math-optimizations")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fassociative-math")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -freciprocal-math")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fassociative-math")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -freciprocal-math")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -ffinite-math-only")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fno-signed-zeros")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fno-trapping-math")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -frounding-math")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsingle-precision-constant")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fcx-limited-range")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fcx-fortran-rules")

file(GLOB SOURCE_FILES
        ./*.h
        ./*.cpp
        ./systems/rendersystem/*.h
        ./systems/rendersystem/*.cpp)

include_directories(lib/glm)

add_subdirectory(utils)

add_executable(ComponentSystem ${SOURCE_FILES})