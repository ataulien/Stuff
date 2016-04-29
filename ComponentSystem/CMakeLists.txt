cmake_minimum_required(VERSION 2.4)
project(ComponentSystem)

set(CMAKE_CXX_STANDARD 11)

file(GLOB SOURCE_FILES
        ./*.cpp)
add_executable(ComponentSystem ${SOURCE_FILES} StaticReferencedAllocator.h MemUtils.h)