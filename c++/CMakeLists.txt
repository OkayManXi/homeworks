cmake_minimum_required(VERSION 2.8.3)
project(Beverage_dispensers)

set(CMAKE_BUILD_TYPE "Release")
set(CMAKE_CXX_FLAGS "-std=c++11")

INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR}/include)

add_executable(Beverage_dispensers
    main.cpp
    src/account.cpp
    src/cmachine.cpp
    src/customer.cpp
    src/drink.cpp
    src/supplier.cpp)