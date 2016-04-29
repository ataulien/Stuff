#pragma once
#include <cstdint>
#include "FreeList.h"
#include "MemUtils.h"
#include <assert.h>
#include <cstring>

namespace Memory
{
    template<int N1, int N2>
    struct GenericHandle
    {
        uint32_t index : N1;
        uint32_t generation : N2;
    };

    /**
     * @param T Type of data stored in the allocator
     * @param NUM Number of elements statically allocated
     */
    template<typename T, unsigned int NUM>
    class StaticReferencedAllocator
    {
    public:
        //typedef GenericHandle<numberOfBits(NUM), sizeof(void*) - numberOfBits(NUM)> Handle;
        typedef GenericHandle<12, 20> Handle;

        StaticReferencedAllocator() :
                m_FreeList(m_InternalHandles, m_InternalHandles + NUM, sizeof(m_InternalHandles[0]), NUM, sizeof(m_InternalHandles[0]), 0),
                m_LastInternalHandle(nullptr)
        {
            // Initialize handles
            for (size_t i = 0; i < NUM; i++) {
                m_InternalHandles[i].m_Handle.index = (1U << 12) - 1;
                m_InternalHandles[i].m_Handle.generation = 0;
            }
        }

        Handle createObject()
        {
            assert(m_FreeList.getNumObtainedElements() != NUM);

            // Use the element at the end of the array as target
            size_t idx = m_FreeList.getNumObtainedElements();

            // Get a new handle from the free-list
            auto* handle = m_FreeList.obtainElement();
            handle->m_Handle.index = static_cast<uint32_t>(idx); // TODO: Care for bit-size of 'index'
            // (Don't need to touch the generation, only needed on deletion)

            // Store this as the new handle to the end of the list
            m_LastInternalHandle = handle;

            // Create output handle
            Handle hOut;
            hOut.index = static_cast<uint32_t>(handle - m_InternalHandles);
            hOut.generation = handle->m_Handle.generation;

            // Connect element and internal handle
            m_ElementsToInternalHandles[idx] = hOut.index;

            return hOut;
        }

        T& getElement(const Handle& h)
        {
            assert(m_InternalHandles[h.index].m_Handle.generation == h.generation);

            return m_Elements[m_InternalHandles[h.index].m_Handle.index];
        }

        void removeObject(const Handle& h)
        {
            // Check if the handle is still valid. If not, we are accessing a different object!
            assert(m_InternalHandles[h.index].m_Handle.generation == h.generation);
            assert(m_LastInternalHandle != nullptr); // Must have at least one handle in there

            // Get actual index of handle-target
            uint32_t actIdx = m_InternalHandles[h.index].m_Handle.index;

            // Overwrite this element with the last one
            memcpy(&m_Elements[actIdx], &m_Elements[m_LastInternalHandle->m_Handle.index], sizeof(T));

            // Fix the handle of the last element
            m_LastInternalHandle->m_Handle.index = actIdx;
            m_ElementsToInternalHandles[actIdx] = m_LastInternalHandle - m_InternalHandles;

            // Increase generation of old element
            m_InternalHandles[h.index].m_Handle.generation++;

            // Return the handle to the free-list
            m_FreeList.returnElement(&m_InternalHandles[h.index]);

            // Get new back-object
            if(m_FreeList.getNumObtainedElements() > 0)
                m_LastInternalHandle = &m_InternalHandles[m_ElementsToInternalHandles[m_FreeList.getNumObtainedElements() - 1]];
            else
                m_LastInternalHandle = nullptr;
        }

    private:
        /** Actual element data */
        T m_Elements[NUM]; // TODO: Might want this on the heap!

        /** Contains the index of an internal handle for each element */
        size_t m_ElementsToInternalHandles[NUM];

        /** Helper-struct to get around FreeList needing at least the size of a pointer to operate */
        struct FLHandle
        {
            void* m_Next; // Don't let the free-list overwrite our generation
            Handle m_Handle;
        };

        /** Make handles with enough bits to hold NUM indices. Use the rest for generations. */
        FLHandle m_InternalHandles[NUM];

        /** Handle to the last element created */
        FLHandle* m_LastInternalHandle;

        /** List of free handles */
        FreeList<FLHandle> m_FreeList;
    };
}