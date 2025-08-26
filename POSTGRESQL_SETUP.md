# 🐘 Configuração PostgreSQL - CRM Profissional

## 📋 Sobre a Configuração

O sistema foi desenvolvido para funcionar tanto com **SQLite** (desenvolvimento) quanto com **PostgreSQL** (produção). Por padrão, está configurado para SQLite para facilitar o primeiro uso.

## 🚀 Como Migrar para PostgreSQL

### 1️⃣ **Requisitos**
- PostgreSQL instalado e rodando
- Credenciais de acesso configuradas

### 2️⃣ **Suas Credenciais**
Conforme informado, suas credenciais são:
```env
PGHOST=localhost
PGPORT=5432
PGUSER=postgres
PGPASSWORD=xbala
PGDATABASE=db_crm
```

### 3️⃣ **Configuração Automática**

Quando o PostgreSQL estiver disponível, execute:

```bash
# Automaticamente detecta PostgreSQL e configura
python3 setup_postgresql.py
```

**O script irá:**
- ✅ Verificar conexão PostgreSQL
- ✅ Criar banco `db_crm` se não existir
- ✅ Criar todas as tabelas necessárias
- ✅ Configurar o Django para PostgreSQL
- ✅ Executar migrações
- ✅ Criar superusuário admin/admin123

### 4️⃣ **Configuração Manual**

Se preferir configurar manualmente:

1. **Certifique-se que PostgreSQL está rodando**
2. **Execute o script de criação do banco:**
   ```bash
   python3 db.py
   ```

3. **Atualize o arquivo .env:**
   ```env
   USE_SQLITE=False
   ```

4. **Execute as migrações:**
   ```bash
   python3 manage.py migrate
   python3 manage.py createsuperuser
   ```

## 📁 **Arquivos de Configuração**

### 🔧 **db.py**
Script completo que:
- Conecta ao PostgreSQL
- Cria banco `db_crm`
- Cria todas as tabelas necessárias
- Lista tabelas criadas

### ⚙️ **setup_postgresql.py**
Script automático que:
- Detecta disponibilidade do PostgreSQL
- Configura automaticamente todo o sistema
- Fallback para SQLite se PostgreSQL indisponível

### 📝 **.env**
Arquivo de configuração com suas credenciais:
```env
# PostgreSQL
PGHOST=localhost
PGPORT=5432
PGUSER=postgres
PGPASSWORD=xbala
PGDATABASE=db_crm

# SQLite (temporário)
USE_SQLITE=True  # Mude para False para PostgreSQL
```

## 🔄 **Status Atual**

**✅ Sistema Funcionando com SQLite**
- Banco: `bd_crm.sqlite3`
- Usuário: `admin`
- Senha: `admin123`
- URL: http://localhost:8000

## 🐘 **Tabelas PostgreSQL**

O script `db.py` cria automaticamente:

### 🔐 **Autenticação Django**
- `auth_user`, `auth_group`, `auth_permission`
- `django_session`, `django_admin_log`

### 👥 **Módulo Clientes**
- `clientes_cliente` - Dados principais dos clientes
- `clientes_contato` - Contatos por cliente

### 💰 **Módulo Vendas**
- `vendas_produto` - Catálogo de produtos
- `vendas_oportunidade` - Pipeline de vendas
- `vendas_venda` - Vendas realizadas
- `vendas_itemvenda` - Itens das vendas

### ✅ **Módulo Tarefas**
- `tarefas_tarefa` - Sistema de tarefas
- `tarefas_anotacao` - Anotações das tarefas
- `tarefas_atividade` - Histórico de atividades
- `tarefas_agenda` - Agenda de compromissos

## 🔧 **Comandos Úteis**

```bash
# Verificar status do PostgreSQL
sudo systemctl status postgresql

# Iniciar PostgreSQL
sudo systemctl start postgresql

# Conectar ao PostgreSQL
psql -h localhost -U postgres -d db_crm

# Configurar CRM automaticamente
python3 setup_postgresql.py

# Criar banco manualmente
python3 db.py

# Executar com PostgreSQL
USE_SQLITE=False python3 manage.py runserver
```

## 🎯 **Benefícios do PostgreSQL**

- **Performance superior** para dados grandes
- **Integridade referencial** robusta
- **Backup e restore** profissionais
- **Concurrent users** sem problemas
- **Extensibilidade** para funcionalidades avançadas

## 📞 **Suporte**

Em caso de problemas:
1. Verifique se PostgreSQL está rodando
2. Confirme as credenciais no arquivo `.env`
3. Execute `python3 setup_postgresql.py` para diagnóstico
4. Verifique logs em `crm_debug.log`

---

🚀 **O sistema está pronto para funcionar com PostgreSQL assim que estiver disponível!**