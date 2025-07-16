#!/bin/bash
set -e

echo "🔧 Устанавливаем pre-commit хуки..."

if ! command -v pre-commit &> /dev/null; then
    echo "❌ pre-commit не установлен. Установите через 'pip install pre-commit'"
    exit 1
fi

pre-commit install --install-hooks
echo "✅ Хуки установлены."
