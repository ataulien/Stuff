#include <vector>

namespace Mesh
{

    template<typename V, typename I, typename VHDL, typename IHDL>
    struct StaticMeshInfo
    {
        // Global information
        std::vector<V> m_Vertices;
        std::vector<I> m_Indices;  
        
        VHDL m_VertexBufferHandle;
        IHDL m_IndexBufferHandle;
    };

    template<typename I>
    struct SubmeshVxInfo
    {
        I m_StartIndex;
        I m_NumIndices;
    };

    /**
    * Static mesh
    * @param V Vertex-typename
    * @param I Index-typename
    * @param M Material-typename
    * @param VHDL Vertexbuffer handle typename
    * @param IHDL Indexbuffer handle typename
    * @param NMSH Number of submeshes stored here. 0 for dynamic!
    */
    template<typename V, typename I, typename M, typename VHDL, typename IHDL, int NMSH>
    struct StaticMesh : public StaticMeshInfo<V,I, VHDL, IHDL>
    {
        // Submesh-Information
        SubmeshVxInfo<I> m_SubmeshStarts[NMSH];
        M m_SubmeshMaterials[NMSH];
        
        enum { NUM_MESHES = NMSH };
    };

    /**
    * Static mesh with unset amount of submeshes
    */
    template<typename V, typename I, typename M, typename VHDL, typename IHDL>
    struct StaticMesh<V, I, M, VHDL, IHDL, 0> : public StaticMeshInfo<V,I, VHDL, IHDL>
    {
        // Submesh information
        std::vector<SubmeshVxInfo<I>> m_SubmeshStarts;
        std::vector<M> m_SubmeshMaterials;
    };
}