#pragma once
#include <inttypes.h>

namespace Mesh
{
    struct float3
    {
        union
        {
            struct{ float x,y,z; };
            float v[3];
        };
    };
    
    struct float2
    {
        union
        {
            struct{ float x,y; };
            float v[2];
        };
    };
    
    struct PositionVertex
    {
        float3 Position;
    };
    
    struct UVVertex
    {
        float3 Position;
        float2 TexCoord;
    };
    
    struct UVNormVertex
    {
        float3 Position;
        float2 TexCoord;
        float3 Normal;
    };
    
    struct UVNormColorVertex
    {
        float3 Position;
        float2 TexCoord;
        float3 Normal;  
        uint32_t Color;
    };
}