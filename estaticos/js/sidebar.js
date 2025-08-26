/*
CRM Profissional - Sidebar JavaScript
Controla a animação e comportamento da sidebar
*/

document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.querySelector('.sidebar');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const conteudoPrincipal = document.querySelector('.conteudo-principal');
    
    // Verifica se os elementos existem
    if (!sidebar || !sidebarToggle) {
        return;
    }
    
    // Carrega o estado salvo da sidebar
    const sidebarFechada = localStorage.getItem('sidebarFechada') === 'true';
    if (sidebarFechada) {
        sidebar.classList.add('fechada');
    }
    
    // Toggle da sidebar
    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('fechada');
        
        // Salva o estado no localStorage
        const isFechada = sidebar.classList.contains('fechada');
        localStorage.setItem('sidebarFechada', isFechada);
        
        // Emite evento personalizado para outros componentes
        window.dispatchEvent(new CustomEvent('sidebarToggle', {
            detail: { fechada: isFechada }
        }));
    });
    
    // Auto-colapsar em telas pequenas
    function verificarTamanhoTela() {
        if (window.innerWidth <= 768) {
            sidebar.classList.add('fechada');
        } else {
            // Restaura o estado salvo em telas maiores
            const sidebarFechada = localStorage.getItem('sidebarFechada') === 'true';
            if (!sidebarFechada) {
                sidebar.classList.remove('fechada');
            }
        }
    }
    
    // Verifica o tamanho da tela ao carregar e redimensionar
    verificarTamanhoTela();
    window.addEventListener('resize', verificarTamanhoTela);
    
    // Marca o item ativo no menu
    function marcarItemAtivo() {
        const navLinks = document.querySelectorAll('.nav-link');
        const currentPath = window.location.pathname;
        
        navLinks.forEach(link => {
            link.classList.remove('ativo');
            
            // Verifica se o href do link corresponde ao caminho atual
            const href = link.getAttribute('href');
            if (href && (currentPath === href || currentPath.startsWith(href + '/'))) {
                link.classList.add('ativo');
            }
        });
    }
    
    // Marca o item ativo ao carregar a página
    marcarItemAtivo();
    
    // Smooth scroll para links internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Efeito de hover nos cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Animação de entrada para elementos
    function animarElementos() {
        const elementos = document.querySelectorAll('.card, .metrica-card');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        elementos.forEach(elemento => {
            observer.observe(elemento);
        });
    }
    
    // Inicia animações
    animarElementos();
    
    // Adiciona comportamento de dropdown se necessário
    const dropdownToggles = document.querySelectorAll('[data-dropdown]');
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            const dropdownMenu = this.nextElementSibling;
            if (dropdownMenu) {
                dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
            }
        });
    });
    
    // Fecha dropdowns ao clicar fora
    document.addEventListener('click', function(e) {
        if (!e.target.closest('[data-dropdown]')) {
            const dropdownMenus = document.querySelectorAll('.dropdown-menu');
            dropdownMenus.forEach(menu => {
                menu.style.display = 'none';
            });
        }
    });
    
    // Tooltip dinâmico para sidebar fechada
    function atualizarTooltips() {
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            const span = link.querySelector('span');
            if (span) {
                link.setAttribute('data-title', span.textContent);
            }
        });
    }
    
    atualizarTooltips();
    
    // Atualiza tooltips quando a sidebar é toggleada
    window.addEventListener('sidebarToggle', atualizarTooltips);
});

// Funções utilitárias globais
window.CRMUtils = {
    // Mostra notificação
    mostrarNotificacao: function(mensagem, tipo = 'info') {
        // Implementar sistema de notificações toast
        console.log(`${tipo.toUpperCase()}: ${mensagem}`);
    },
    
    // Confirma ação
    confirmarAcao: function(mensagem) {
        return confirm(mensagem);
    },
    
    // Formata números para moeda brasileira
    formatarMoeda: function(valor) {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(valor);
    },
    
    // Formata datas para padrão brasileiro
    formatarData: function(data) {
        return new Intl.DateTimeFormat('pt-BR').format(new Date(data));
    }
};