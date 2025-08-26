#!/usr/bin/env python3
"""
Configuração e criação do banco de dados PostgreSQL para o CRM Profissional
Este script conecta ao PostgreSQL e cria todas as tabelas necessárias
"""

import os
import psycopg2
from psycopg2 import sql
import sys

# Database connection parameters
DB_HOST = os.getenv("PGHOST", "localhost")
DB_PORT = os.getenv("PGPORT", "5432")
DB_USER = os.getenv("PGUSER", "postgres")
DB_PASSWORD = os.getenv("PGPASSWORD", "xbala")
DB_NAME = os.getenv("PGDATABASE", "db_crm")

def create_database():
    """Cria o banco de dados se não existir"""
    try:
        # Conecta ao PostgreSQL (banco postgres padrão) para criar o novo banco
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database='postgres'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Verifica se o banco já existe
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_NAME,))
        exists = cursor.fetchone()
        
        if not exists:
            # Cria o banco de dados
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            print(f"✅ Banco de dados '{DB_NAME}' criado com sucesso!")
        else:
            print(f"ℹ️  Banco de dados '{DB_NAME}' já existe.")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Erro ao criar banco de dados: {e}")
        return False

def test_connection():
    """Testa a conexão com o banco de dados"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ Conexão com PostgreSQL estabelecida!")
        print(f"📊 Versão do PostgreSQL: {version}")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def create_tables():
    """Cria todas as tabelas necessárias para o CRM"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        # SQL para criar as tabelas do Django e do CRM
        tables_sql = """
        -- Tabelas do Django Auth
        CREATE TABLE IF NOT EXISTS auth_group (
            id SERIAL PRIMARY KEY,
            name VARCHAR(150) NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS auth_permission (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            content_type_id INTEGER NOT NULL,
            codename VARCHAR(100) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS auth_group_permissions (
            id SERIAL PRIMARY KEY,
            group_id INTEGER NOT NULL,
            permission_id INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS django_content_type (
            id SERIAL PRIMARY KEY,
            app_label VARCHAR(100) NOT NULL,
            model VARCHAR(100) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS auth_user (
            id SERIAL PRIMARY KEY,
            password VARCHAR(128) NOT NULL,
            last_login TIMESTAMPTZ,
            is_superuser BOOLEAN NOT NULL,
            username VARCHAR(150) NOT NULL UNIQUE,
            first_name VARCHAR(150) NOT NULL,
            last_name VARCHAR(150) NOT NULL,
            email VARCHAR(254) NOT NULL,
            is_staff BOOLEAN NOT NULL,
            is_active BOOLEAN NOT NULL,
            date_joined TIMESTAMPTZ NOT NULL
        );

        CREATE TABLE IF NOT EXISTS auth_user_groups (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS auth_user_user_permissions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            permission_id INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS django_admin_log (
            id SERIAL PRIMARY KEY,
            action_time TIMESTAMPTZ NOT NULL,
            object_id TEXT,
            object_repr VARCHAR(200) NOT NULL,
            action_flag SMALLINT NOT NULL,
            change_message TEXT NOT NULL,
            content_type_id INTEGER,
            user_id INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS django_session (
            session_key VARCHAR(40) NOT NULL PRIMARY KEY,
            session_data TEXT NOT NULL,
            expire_date TIMESTAMPTZ NOT NULL
        );

        CREATE TABLE IF NOT EXISTS django_migrations (
            id SERIAL PRIMARY KEY,
            app VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            applied TIMESTAMPTZ NOT NULL
        );

        -- Tabela de Clientes
        CREATE TABLE IF NOT EXISTS clientes_cliente (
            id SERIAL PRIMARY KEY,
            nome_completo VARCHAR(200) NOT NULL,
            nome_fantasia VARCHAR(200),
            tipo_pessoa VARCHAR(2) NOT NULL DEFAULT 'PF',
            cpf_cnpj VARCHAR(20) NOT NULL UNIQUE,
            rg_inscricao VARCHAR(20),
            email VARCHAR(254),
            telefone VARCHAR(20),
            celular VARCHAR(20),
            cep VARCHAR(10),
            endereco VARCHAR(300),
            numero VARCHAR(10),
            complemento VARCHAR(100),
            bairro VARCHAR(100),
            cidade VARCHAR(100),
            estado VARCHAR(2),
            status VARCHAR(10) NOT NULL DEFAULT 'potencial',
            segmento VARCHAR(100),
            origem VARCHAR(100),
            observacoes TEXT,
            responsavel_id INTEGER,
            data_cadastro TIMESTAMPTZ NOT NULL,
            data_atualizacao TIMESTAMPTZ NOT NULL,
            ativo BOOLEAN NOT NULL DEFAULT TRUE
        );

        -- Tabela de Contatos
        CREATE TABLE IF NOT EXISTS clientes_contato (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            cargo VARCHAR(100),
            email VARCHAR(254),
            telefone VARCHAR(20),
            celular VARCHAR(20),
            observacoes TEXT,
            principal BOOLEAN NOT NULL DEFAULT FALSE,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            data_cadastro TIMESTAMPTZ NOT NULL,
            cliente_id INTEGER NOT NULL
        );

        -- Tabela de Produtos
        CREATE TABLE IF NOT EXISTS vendas_produto (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(200) NOT NULL,
            descricao TEXT,
            codigo VARCHAR(50) NOT NULL UNIQUE,
            preco_unitario DECIMAL(10,2) NOT NULL,
            categoria VARCHAR(100),
            unidade_medida VARCHAR(10) NOT NULL DEFAULT 'UN',
            estoque_atual INTEGER NOT NULL DEFAULT 0,
            estoque_minimo INTEGER NOT NULL DEFAULT 0,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            data_cadastro TIMESTAMPTZ NOT NULL
        );

        -- Tabela de Oportunidades
        CREATE TABLE IF NOT EXISTS vendas_oportunidade (
            id SERIAL PRIMARY KEY,
            titulo VARCHAR(200) NOT NULL,
            valor_estimado DECIMAL(12,2) NOT NULL,
            probabilidade INTEGER NOT NULL DEFAULT 50,
            status VARCHAR(20) NOT NULL DEFAULT 'prospectando',
            fase_funil VARCHAR(20) NOT NULL DEFAULT 'inicial',
            data_inicio DATE NOT NULL,
            data_fechamento_prevista DATE NOT NULL,
            data_fechamento_real DATE,
            descricao TEXT,
            origem VARCHAR(100),
            concorrentes TEXT,
            observacoes TEXT,
            data_cadastro TIMESTAMPTZ NOT NULL,
            data_atualizacao TIMESTAMPTZ NOT NULL,
            cliente_id INTEGER NOT NULL,
            responsavel_id INTEGER
        );

        -- Tabela de Vendas
        CREATE TABLE IF NOT EXISTS vendas_venda (
            id SERIAL PRIMARY KEY,
            numero VARCHAR(20) NOT NULL UNIQUE,
            data_venda DATE NOT NULL,
            status VARCHAR(15) NOT NULL DEFAULT 'orcamento',
            valor_total DECIMAL(12,2) NOT NULL DEFAULT 0,
            desconto DECIMAL(10,2) NOT NULL DEFAULT 0,
            observacoes TEXT,
            data_cadastro TIMESTAMPTZ NOT NULL,
            data_atualizacao TIMESTAMPTZ NOT NULL,
            cliente_id INTEGER NOT NULL,
            oportunidade_id INTEGER,
            vendedor_id INTEGER
        );

        -- Tabela de Itens de Venda
        CREATE TABLE IF NOT EXISTS vendas_itemvenda (
            id SERIAL PRIMARY KEY,
            quantidade DECIMAL(10,2) NOT NULL,
            preco_unitario DECIMAL(10,2) NOT NULL,
            desconto_item DECIMAL(10,2) NOT NULL DEFAULT 0,
            observacoes VARCHAR(300),
            venda_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL
        );

        -- Tabela de Tarefas
        CREATE TABLE IF NOT EXISTS tarefas_tarefa (
            id SERIAL PRIMARY KEY,
            titulo VARCHAR(200) NOT NULL,
            descricao TEXT,
            tipo VARCHAR(15) NOT NULL DEFAULT 'outro',
            status VARCHAR(15) NOT NULL DEFAULT 'pendente',
            prioridade VARCHAR(10) NOT NULL DEFAULT 'media',
            data_vencimento TIMESTAMPTZ NOT NULL,
            data_conclusao TIMESTAMPTZ,
            tempo_estimado INTEGER,
            lembrete BOOLEAN NOT NULL DEFAULT FALSE,
            data_lembrete TIMESTAMPTZ,
            data_cadastro TIMESTAMPTZ NOT NULL,
            data_atualizacao TIMESTAMPTZ NOT NULL,
            responsavel_id INTEGER NOT NULL,
            cliente_id INTEGER,
            oportunidade_id INTEGER,
            criado_por_id INTEGER
        );

        -- Tabela de Anotações
        CREATE TABLE IF NOT EXISTS tarefas_anotacao (
            id SERIAL PRIMARY KEY,
            conteudo TEXT NOT NULL,
            data_criacao TIMESTAMPTZ NOT NULL,
            tarefa_id INTEGER NOT NULL,
            autor_id INTEGER NOT NULL
        );

        -- Tabela de Atividades
        CREATE TABLE IF NOT EXISTS tarefas_atividade (
            id SERIAL PRIMARY KEY,
            titulo VARCHAR(200) NOT NULL,
            descricao TEXT,
            tipo VARCHAR(20) NOT NULL DEFAULT 'outro',
            data_atividade TIMESTAMPTZ NOT NULL,
            data_cadastro TIMESTAMPTZ NOT NULL,
            usuario_id INTEGER NOT NULL,
            cliente_id INTEGER,
            oportunidade_id INTEGER,
            tarefa_id INTEGER
        );

        -- Tabela de Agenda
        CREATE TABLE IF NOT EXISTS tarefas_agenda (
            id SERIAL PRIMARY KEY,
            titulo VARCHAR(200) NOT NULL,
            descricao TEXT,
            tipo VARCHAR(15) NOT NULL DEFAULT 'reuniao',
            data_inicio TIMESTAMPTZ NOT NULL,
            data_fim TIMESTAMPTZ NOT NULL,
            dia_inteiro BOOLEAN NOT NULL DEFAULT FALSE,
            local VARCHAR(300),
            endereco TEXT,
            lembrete BOOLEAN NOT NULL DEFAULT TRUE,
            minutos_lembrete INTEGER NOT NULL DEFAULT 15,
            data_cadastro TIMESTAMPTZ NOT NULL,
            data_atualizacao TIMESTAMPTZ NOT NULL,
            organizador_id INTEGER NOT NULL,
            cliente_id INTEGER,
            oportunidade_id INTEGER
        );

        -- Tabela many-to-many para participantes da agenda
        CREATE TABLE IF NOT EXISTS tarefas_agenda_participantes (
            id SERIAL PRIMARY KEY,
            agenda_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL
        );
        """
        
        # Executa os comandos SQL
        cursor.execute(tables_sql)
        conn.commit()
        
        print("✅ Todas as tabelas foram criadas com sucesso!")
        
        # Lista as tabelas criadas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print("\n📋 Tabelas criadas:")
        for table in tables:
            print(f"   • {table[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Configurando banco de dados PostgreSQL para CRM Profissional")
    print(f"📍 Host: {DB_HOST}:{DB_PORT}")
    print(f"👤 Usuário: {DB_USER}")
    print(f"🗄️  Banco: {DB_NAME}")
    print("-" * 60)
    
    # Criar banco de dados
    if not create_database():
        sys.exit(1)
    
    # Testar conexão
    if not test_connection():
        sys.exit(1)
    
    # Criar tabelas
    if not create_tables():
        sys.exit(1)
    
    print("\n🎉 Configuração do banco de dados concluída com sucesso!")
    print("📝 Próximos passos:")
    print("   1. Execute: python manage.py migrate")
    print("   2. Execute: python manage.py createsuperuser")
    print("   3. Execute: python manage.py runserver")

if __name__ == "__main__":
    main()