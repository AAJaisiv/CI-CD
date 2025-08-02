#!/bin/bash

echo "�� Running Unit Tests..."
pytest tests/unit/ -v --cov=src --cov-report=term-missing

echo ""
echo "🔍 Running Code Quality Checks..."
flake8 src/ tests/

echo ""
echo "🎨 Running Code Formatting Check..."
black --check src/ tests/

echo ""
echo "🛡️ Running Security Scan..."
bandit -r src/

echo ""
echo "✅ All tests completed!"