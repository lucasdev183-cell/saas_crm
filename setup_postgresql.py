#!/usr/bin/env python3
"""
Script de configuração para migrar do SQLite para PostgreSQL
CRM Profissional - Sistema de migração de banco de dados
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Exibe banner do script"""
    print("=" * 70)
    print("🚀 CRM Profissional - Configuração PostgreSQL")
    print("=" * 70)

def check_postgresql_connection():
    """Verifica se consegue conectar ao PostgreSQL"""
    try:
        import psycopg2
        from dotenv import load_dotenv
        
        load_dotenv()
        
        conn = psycopg2.connect(
            host=os.getenv("PGHOST", "localhost"),
            port=os.getenv("PGPORT", "5432"),
            user=os.getenv("PGUSER", "postgres"),
            password=os.getenv("PGPASSWORD", "xbala"),
            database="postgres"  # conecta ao banco padrão primeiro
        )
        conn.close()
        print("✅ Conexão com PostgreSQL estabelecida!")
        return True
    except Exception as e:
        print(f"❌ Erro de conexão PostgreSQL: {e}")
        return False

def update_env_file(use_postgres=True):
    """Atualiza o arquivo .env para usar PostgreSQL ou SQLite"""
    env_path = Path(".env")
    
    if env_path.exists():
        content = env_path.read_text()
        
        if use_postgres:
            content = content.replace("USE_SQLITE=True", "USE_SQLITE=False")
        else:
            content = content.replace("USE_SQLITE=False", "USE_SQLITE=True")
        
        env_path.write_text(content)
        db_type = "PostgreSQL" if use_postgres else "SQLite"
        print(f"✅ Arquivo .env atualizado para usar {db_type}")

def run_db_script():
    """Executa o script db.py para criar o banco PostgreSQL"""
    try:
        result = subprocess.run([sys.executable, "db.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Script db.py executado com sucesso!")
            print(result.stdout)
        else:
            print("❌ Erro ao executar db.py:")
            print(result.stderr)
            return False
        return True
    except Exception as e:
        print(f"❌ Erro ao executar db.py: {e}")
        return False

def run_django_commands():
    """Executa comandos Django necessários"""
    commands = [
        ["python3", "manage.py", "migrate"],
        ["python3", "manage.py", "collectstatic", "--noinput"]
    ]
    
    for cmd in commands:
        try:
            print(f"🔄 Executando: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {cmd[1]} executado com sucesso!")
            else:
                print(f"❌ Erro em {cmd[1]}:")
                print(result.stderr)
                return False
        except Exception as e:
            print(f"❌ Erro ao executar {' '.join(cmd)}: {e}")
            return False
    
    return True

def create_superuser():
    """Cria ou atualiza o superusuário"""
    try:
        script = """
from django.contrib.auth.models import User
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@crm.com',
        'is_staff': True,
        'is_superuser': True,
        'is_active': True
    }
)
admin_user.set_password('admin123')
admin_user.save()
print(f"Usuário admin {'criado' if created else 'atualizado'} com sucesso!")
"""
        
        result = subprocess.run([
            "python3", "manage.py", "shell", "-c", script
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Superusuário configurado!")
            print("👤 Credenciais: admin / admin123")
        else:
            print("❌ Erro ao criar superusuário:")
            print(result.stderr)
            return False
        return True
    except Exception as e:
        print(f"❌ Erro ao criar superusuário: {e}")
        return False

def main():
    """Função principal"""
    print_banner()
    
    print("\n🔍 Verificando disponibilidade do PostgreSQL...")
    
    if check_postgresql_connection():
        print("\n🎯 PostgreSQL disponível! Configurando...")
        
        # Atualiza .env para PostgreSQL
        update_env_file(use_postgres=True)
        
        # Executa script de criação do banco
        if run_db_script():
            print("\n🔄 Executando comandos Django...")
            if run_django_commands():
                print("\n👤 Configurando superusuário...")
                if create_superuser():
                    print("\n🎉 Configuração PostgreSQL concluída com sucesso!")
                    print("\n📋 Resumo:")
                    print("   • Banco PostgreSQL: db_crm")
                    print("   • Usuário: admin")
                    print("   • Senha: admin123")
                    print("   • URL: http://localhost:8000")
                    print("\n🚀 Execute: python manage.py runserver")
                else:
                    print("❌ Falha na configuração do superusuário")
            else:
                print("❌ Falha nos comandos Django")
        else:
            print("❌ Falha na criação do banco PostgreSQL")
    
    else:
        print("\n⚠️  PostgreSQL não disponível. Usando SQLite...")
        
        # Atualiza .env para SQLite
        update_env_file(use_postgres=False)
        
        print("\n🔄 Executando comandos Django com SQLite...")
        if run_django_commands():
            print("\n👤 Configurando superusuário...")
            if create_superuser():
                print("\n✅ Sistema configurado com SQLite!")
                print("\n📋 Resumo:")
                print("   • Banco SQLite: bd_crm.sqlite3")
                print("   • Usuário: admin")
                print("   • Senha: admin123")
                print("   • URL: http://localhost:8000")
                print("\n🚀 Execute: python manage.py runserver")
                print("\n💡 Para usar PostgreSQL mais tarde:")
                print("   1. Configure o PostgreSQL")
                print("   2. Execute: python setup_postgresql.py")
            else:
                print("❌ Falha na configuração do superusuário")
        else:
            print("❌ Falha nos comandos Django")

if __name__ == "__main__":
    main()