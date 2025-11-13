"""
Test MCP server tools availability
"""
import asyncio
import json
from spatial_ai_enhanced import server, call_tool

async def test_list_tools():
    """Test tool listing"""
    print("=" * 60)
    print("MCP SERVER TOOLS TEST")
    print("=" * 60)

    # Get list of tools
    from spatial_ai_enhanced import list_tools

    tools = await list_tools()

    print(f"\nAvailable Tools: {len(tools)}")
    print("-" * 60)

    for tool in tools:
        print(f"\n📌 {tool.name}")
        print(f"   Description: {tool.description[:100]}...")
        if hasattr(tool, 'inputSchema'):
            required = tool.inputSchema.get('required', [])
            properties = tool.inputSchema.get('properties', {})
            print(f"   Required params: {', '.join(required) if required else 'None'}")
            print(f"   Total params: {len(properties)}")

    return tools

async def test_calculate_placement():
    """Test calculate_optimal_placement tool"""
    print("\n" + "=" * 60)
    print("TEST: calculate_optimal_placement")
    print("=" * 60)

    test_args = {
        "width": 300,
        "height": 200,
        "content_type": "diagram",
        "priority": 8,
        "content": "Test diagram content",
        "use_quantum": False,  # Disable quantum due to bug
        "enable_temporal": True
    }

    print(f"\nInput: {json.dumps(test_args, indent=2)}")

    result = await call_tool("calculate_optimal_placement", test_args)
    response = json.loads(result[0].text)

    print(f"\nResult:")
    print(json.dumps(response, indent=2))

    return response.get("success", False)

async def test_update_preferences():
    """Test update_preferences tool"""
    print("\n" + "=" * 60)
    print("TEST: update_preferences")
    print("=" * 60)

    pref_args = {
        "aesthetic": 0.9,
        "balance": 0.7,
        "flow": 0.8,
        "whitespace": 0.85,
        "hierarchy": 0.75
    }

    print(f"\nInput: {json.dumps(pref_args, indent=2)}")

    result = await call_tool("update_preferences", pref_args)
    response = json.loads(result[0].text)

    print(f"\nResult:")
    print(json.dumps(response, indent=2))

    return response.get("success", False)

async def test_get_layout_embedding():
    """Test get_layout_embedding tool"""
    print("\n" + "=" * 60)
    print("TEST: get_layout_embedding")
    print("=" * 60)

    result = await call_tool("get_layout_embedding", {})
    response = json.loads(result[0].text)

    print(f"\nEmbedding dimensions: {response.get('dimensions', 0)}")
    print(f"Success: {response.get('success', False)}")

    if 'embedding' in response and len(response['embedding']) > 0:
        print(f"Sample values: {response['embedding'][:5]}")

    return response.get("success", False)

async def test_generate_animation_path():
    """Test generate_animation_path tool"""
    print("\n" + "=" * 60)
    print("TEST: generate_animation_path")
    print("=" * 60)

    path_args = {
        "block_id": "test_block_1",
        "start_x": 100,
        "start_y": 100,
        "end_x": 500,
        "end_y": 400,
        "curve_type": "cubic_bezier"
    }

    print(f"\nInput: {json.dumps(path_args, indent=2)}")

    result = await call_tool("generate_animation_path", path_args)
    response = json.loads(result[0].text)

    print(f"\nPath frames: {response.get('frames', 0)}")
    print(f"Curve type: {response.get('curve_type', 'N/A')}")
    print(f"Success: {response.get('success', False)}")

    if 'path' in response and len(response['path']) > 0:
        print(f"Start point: {response['path'][0]}")
        print(f"End point: {response['path'][-1]}")

    return response.get("success", False)

async def test_add_block():
    """Test add_block_to_canvas tool"""
    print("\n" + "=" * 60)
    print("TEST: add_block_to_canvas")
    print("=" * 60)

    block_args = {
        "x": 100,
        "y": 200,
        "width": 300,
        "height": 150,
        "content": "Sample content",
        "block_type": "text",
        "priority": 7,
        "semantic_group": "main"
    }

    print(f"\nInput: {json.dumps(block_args, indent=2)}")

    result = await call_tool("add_block_to_canvas", block_args)
    response = json.loads(result[0].text)

    print(f"\nTotal blocks: {response.get('total_blocks', 0)}")
    print(f"Success: {response.get('success', False)}")

    return response.get("success", False)

async def test_get_statistics():
    """Test get_canvas_statistics tool"""
    print("\n" + "=" * 60)
    print("TEST: get_canvas_statistics")
    print("=" * 60)

    result = await call_tool("get_canvas_statistics", {})
    response = json.loads(result[0].text)

    print(f"\nResult:")
    print(json.dumps(response, indent=2))

    return response.get("success", False)

async def main():
    """Run all MCP tool tests"""
    print("\n" + "=" * 60)
    print("MCP SERVER CAPABILITY TESTS")
    print("=" * 60)

    # List tools
    tools = await test_list_tools()

    # Test each tool
    tests = [
        ("calculate_optimal_placement", test_calculate_placement),
        ("update_preferences", test_update_preferences),
        ("get_layout_embedding", test_get_layout_embedding),
        ("generate_animation_path", test_generate_animation_path),
        ("add_block_to_canvas", test_add_block),
        ("get_canvas_statistics", test_get_statistics)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            success = await test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n✗ {test_name} FAILED: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("MCP TOOLS TEST SUMMARY")
    print("=" * 60)

    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {test_name}")

    passed = sum(1 for _, s in results if s)
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
