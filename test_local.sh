#!/bin/bash
# test_local.sh - Testando o cofre digital localmente

# Interrompe o script em caso de qualquer erro
set -e

echo "🚀 Iniciando teste do Cofre Digital..."

# 1. Construindo a imagem
echo "📦 Construindo container image..."
docker build -f docker/Dockerfile -t cofre-digital-local .

# 2. Garantir que não existam containers antigos com o mesmo nome
docker stop cofre-test 2>/dev/null || true
docker rm cofre-test 2>/dev/null || true

# 3. Testando com secrets de desenvolvimento
echo "⚙️  Iniciando aplicação com secrets de dev..."
docker run -d --name cofre-test \
  -p 5000:5000 \
  -e ENVIRONMENT=test \
  -e DB_HOST=test-db.local \
  -e DB_USER=test_user \
  -e DB_PASSWORD=test_password_123 \
  -e EXTERNAL_API_KEY=test_key_abcd1234 \
  cofre-digital-local

# 4. Aguardando inicialização
echo "⏳ Aguardando 5 segundos para inicialização..."
sleep 5

# 5. Testando endpoints
echo "🔍 Testando endpoints..."
# Verifica se o jq está instalado, senão exibe o texto puro
if command -v jq &> /dev/null; then
    curl -s http://localhost:5000/ | jq .
    curl -s http://localhost:5000/database | jq .
    curl -s http://localhost:5000/api-key | jq .
else
    curl -s http://localhost:5000/
    curl -s http://localhost:5000/database
    curl -s http://localhost:5000/api-key
fi

# 6. Verificando logs (devem estar mascarados)
echo -e "\n📋 Verificando logs (secrets devem estar mascarados)..."
docker logs cofre-test

# 7. Limpeza
echo -e "\n🧹 Limpando ambiente..."
docker stop cofre-test
docker rm cofre-test

echo "✅ Teste local concluído com sucesso!"
