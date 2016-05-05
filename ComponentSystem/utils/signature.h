#pragma once
#include <cstdint>

/**
 * @brief Defines a trait to check for the existance of a static function, which can be used like this:
 *        DEFINE_HAS_SIGNATURE(has_foo, T::foo, void (*)(void));
 *        ...
 *        static_assert(has_foo<StaticFoo>::value, "Unexpected value");
 *
 *        Source: https://ideone.com/nDlFUE
 */
#define DEFINE_HAS_SIGNATURE(traitsName, funcName, signature)               \
    template <typename U>                                                   \
    class traitsName                                                        \
    {                                                                       \
    private:                                                                \
        template<typename T, T> struct helper;                              \
        template<typename T>                                                \
        static std::uint8_t check(helper<signature, &funcName>*);           \
        template<typename T> static std::uint16_t check(...);               \
    public:                                                                 \
        static                                                              \
        constexpr bool value = sizeof(check<U>(0)) == sizeof(std::uint8_t); \
    }
