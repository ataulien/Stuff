#pragma once
#include "Entities.h"

namespace Components
{
    namespace Actions
    {
        namespace BBox
        {
            /**
             * @param bxs Array of BBoxComponents
             * @param checkIdx Array of indices to the BBoxComponents to check
             * @param numCheckIdx Number of indices inside the checkIdx-array
             * @param outIndices [out] Array of the same size as checkIdx to contain indices to the visible entities
             * @param numVisible [out] Number of valid indices inside outIndices
             * TODO: Add actual camera-information
             */
            void frustumVisibilityCheck(const BBoxComponent* bxs, const size_t* checkIdx, const size_t numCheckIdx, size_t* outIndices, size_t& numVisible)
            {
                size_t nv = 0;
                for(size_t i=0;i<numCheckIdx;i++)
                {
                    size_t c = checkIdx[i];

                    //std::cout << "Dist: " << Math::float3::distanceSquared((bxs[c].m_BBox3D.min + bxs[c].m_BBox3D.max) * 0.5f, Math::float3(0.0f,0.0f,0.0f)) << std::endl;

                    const float dist = 1000.0f * 1000.0f;
                    if(Math::float3::distanceSquared((bxs[c].m_BBox3D.min + bxs[c].m_BBox3D.max) * 0.5f, Math::float3(0.0f,0.0f,0.0f)) < dist
                       && Math::float3::distanceSquared((bxs[c].m_BBox3D.min + bxs[c].m_BBox3D.max) * 0.5f, Math::float3(1.0f,0.0f,0.0f)) < dist
                       && Math::float3::distanceSquared((bxs[c].m_BBox3D.min + bxs[c].m_BBox3D.max) * 0.5f, Math::float3(2.0f,0.0f,0.0f)) < dist
                       && Math::float3::distanceSquared((bxs[c].m_BBox3D.min + bxs[c].m_BBox3D.max) * 0.5f, Math::float3(3.0f,0.0f,0.0f)) < dist
                       && Math::float3::distanceSquared((bxs[c].m_BBox3D.min + bxs[c].m_BBox3D.max) * 0.5f, Math::float3(4.0f,0.0f,0.0f)) < dist
                       && Math::float3::distanceSquared((bxs[c].m_BBox3D.min + bxs[c].m_BBox3D.max) * 0.5f, Math::float3(5.0f,0.0f,0.0f)) < dist)
                    {
                        outIndices[nv] = c;
                        nv++;
                    }
                }

                numVisible = nv;
            }
        }
    }
}