# 🚀 CRM Profissional

Sistema completo de CRM (Customer Relationship Management) desenvolvido em Django, com interface moderna e intuitiva em português brasileiro.

## 📋 Funcionalidades

### 🏢 Gestão de Clientes
- Cadastro completo de clientes (PF/PJ)
- Histórico de contatos e interações
- Status e segmentação de clientes
- Controle de informações comerciais

### 💰 Gestão de Vendas
- Pipeline de oportunidades
- Controle de vendas e orçamentos
- Catálogo de produtos com controle de estoque
- Funil de vendas interativo
- Métricas de conversão

### ✅ Gestão de Tarefas
- Sistema completo de tarefas
- Agenda de compromissos
- Controle de prioridades
- Histórico de atividades
- Lembretes e notificações

### 📊 Dashboard e Relatórios
- Painel principal com métricas em tempo real
- Gráficos interativos
- Relatórios personalizados
- KPIs de vendas e conversão

## 🎨 Interface

- **Design moderno e limpo** com paleta de cores profissional
- **Sidebar animada** com navegação intuitiva
- **Layout responsivo** adaptado para desktop e mobile
- **Ícones modernos** com Font Awesome
- **Gráficos interativos** com Chart.js

## 🛠️ Tecnologias

- **Backend**: Django 5.2.5
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (desenvolvimento)
- **Icons**: Font Awesome 6.4
- **Charts**: Chart.js
- **Styles**: CSS Custom Properties (variáveis CSS)

## 🚀 Instalação

### Pré-requisitos
- Python 3.8+
- pip

### Passos de Instalação

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd crm-profissional
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute as migrações**
```bash
python manage.py migrate
```

4. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

5. **Inicie o servidor**
```bash
python manage.py runserver
```

6. **Acesse o sistema**
- Aplicação: http://localhost:8000
- Admin: http://localhost:8000/admin

## 📁 Estrutura do Projeto

```
crm_profissional/
├── clientes/           # App de gestão de clientes
├── vendas/             # App de vendas e produtos  
├── tarefas/            # App de tarefas e agenda
├── dashboard/          # App do painel principal
├── templates/          # Templates HTML
├── estaticos/          # Arquivos CSS/JS/Images
├── crm_profissional/   # Configurações do projeto
└── requirements.txt    # Dependências
```

## 🔧 Configuração

### Settings Principais
- **Idioma**: Português brasileiro (pt-br)
- **Timezone**: America/Sao_Paulo
- **Database**: SQLite (desenvolvimento)
- **Static Files**: Configurado para desenvolvimento

### Apps Incluídos
- `clientes` - Gestão de clientes e contatos
- `vendas` - Vendas, produtos e oportunidades
- `tarefas` - Tarefas, agenda e atividades
- `dashboard` - Painel principal e métricas

## 🎯 Uso

### Acessando o Sistema
1. Faça login com suas credenciais
2. Use a sidebar para navegar entre os módulos
3. O painel principal mostra um resumo das atividades

### Módulos Principais

#### 👥 Clientes
- **Lista**: Visualize todos os clientes
- **Cadastro**: Adicione novos clientes
- **Detalhes**: Veja informações completas
- **Contatos**: Gerencie contatos por cliente

#### 💼 Vendas
- **Oportunidades**: Gerencie o pipeline de vendas
- **Produtos**: Catálogo com controle de estoque
- **Vendas**: Registre e acompanhe vendas

#### 📋 Tarefas
- **Tarefas**: Organize suas atividades
- **Agenda**: Gerencie compromissos
- **Atividades**: Histórico de interações

## 📊 Métricas e KPIs

O sistema fornece métricas importantes como:
- Total de clientes e status
- Vendas e faturamento mensal
- Taxa de conversão
- Valor no pipeline
- Tarefas pendentes e atrasadas

## 🎨 Personalização

### Cores
A paleta de cores pode ser ajustada no arquivo `estaticos/css/estilo.css`:
```css
:root {
    --cor-primaria: #A3B3A3;
    --cor-primaria-escura: #8A9B8A;
    /* ... outras cores */
}
```

### Layout
- Sidebar responsiva com animações
- Grid system personalizado
- Cards com efeitos hover
- Formulários estilizados

## 🔐 Segurança

- Autenticação obrigatória para todas as páginas
- Controle de acesso baseado em usuários
- Validação de dados nos formulários
- Proteção CSRF habilitada

## 📱 Responsividade

O sistema é totalmente responsivo:
- **Desktop**: Layout completo com sidebar expandida
- **Tablet**: Sidebar adaptada
- **Mobile**: Sidebar colapsada automaticamente

## 🛡️ Administração

Acesse o Django Admin em `/admin/` para:
- Gerenciar usuários
- Configurar dados mestre
- Visualizar logs do sistema
- Backup de dados

## 🆕 Próximas Funcionalidades

- [ ] Sistema de notificações push
- [ ] Relatórios em PDF
- [ ] Integração com e-mail
- [ ] API REST completa
- [ ] Dashboard mais avançado
- [ ] Sistema de permissões granular

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para dúvidas, sugestões ou problemas:
- Abra uma issue no GitHub
- Entre em contato via e-mail

---

⭐ **Desenvolvido com foco na experiência do usuário e produtividade empresarial**