import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- Configuração da Página ---
st.set_page_config(page_title="Gestão de Estoque (Memória)", layout="wide", page_icon="📦")

# --- Inicialização dos Dados em Memória (Session State) ---
# Aqui substituímos o Banco de Dados por listas na memória
def init_data():
    if 'db_produtos' not in st.session_state:
        st.session_state['db_produtos'] = [] # Lista de dicionários
        # Criando alguns dados fictícios para não começar vazio
        st.session_state['db_produtos'].append({
            'id': 1, 'nome': 'Notebook Dell', 'categoria': 'Eletrônicos', 
            'descricao': 'i5 8GB', 'quantidade': 10, 'estoque_minimo': 5, 'valor_unitario': 3500.00
        })
        st.session_state['db_produtos'].append({
            'id': 2, 'nome': 'Mouse Sem Fio', 'categoria': 'Acessórios', 
            'descricao': 'Logitech', 'quantidade': 3, 'estoque_minimo': 10, 'valor_unitario': 80.00
        })
        st.session_state['next_prod_id'] = 3 # Contador para gerar IDs

    if 'db_movimentacoes' not in st.session_state:
        st.session_state['db_movimentacoes'] = []
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['user_role'] = None
        st.session_state['username'] = None

init_data()

# --- Funções Auxiliares ---
def get_produtos_df():
    if not st.session_state['db_produtos']:
        return pd.DataFrame(columns=['id', 'nome', 'categoria', 'descricao', 'quantidade', 'estoque_minimo', 'valor_unitario'])
    return pd.DataFrame(st.session_state['db_produtos'])

def get_movimentacoes_df():
    if not st.session_state['db_movimentacoes']:
        return pd.DataFrame(columns=['data_hora', 'produto', 'tipo', 'quantidade', 'usuario'])
    return pd.DataFrame(st.session_state['db_movimentacoes'])

# --- Autenticação ---
def login():
    st.markdown("## 🔐 Login (Versão em Memória)")
    st.info("Dica: Use **admin/admin123** ou **op/op123**")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        
        if st.button("Entrar"):
            if username == "admin" and password == "admin123":
                st.session_state['logged_in'] = True
                st.session_state['user_role'] = 'Administrador'
                st.session_state['username'] = 'admin'
                st.rerun()
            elif username == "op" and password == "op123":
                st.session_state['logged_in'] = True
                st.session_state['user_role'] = 'Operador'
                st.session_state['username'] = 'op'
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")

def logout():
    # Não limpamos db_produtos para não perder dados ao fazer logoff, apenas o status de login
    st.session_state['logged_in'] = False
    st.session_state['user_role'] = None
    st.rerun()

# --- Interface Principal ---
if not st.session_state['logged_in']:
    login()
else:
    # Sidebar
    st.sidebar.title("📦 Estoque RAM")
    st.sidebar.markdown(f"**Usuário:** {st.session_state['username']}")
    st.sidebar.markdown(f"**Nível:** {st.session_state['user_role']}")
    st.sidebar.warning("⚠️ Dados serão perdidos ao recarregar a página (F5).")
    
    options = ["Dashboard", "Consultar Estoque", "Registrar Movimentação"]
    if st.session_state['user_role'] == 'Administrador':
        options.extend(["Cadastro de Produtos", "Histórico Completo"])
    
    options.append("Sair")
    choice = st.sidebar.radio("Menu", options)

    # --- 1. Dashboard ---
    if choice == "Dashboard":
        st.header("📊 Visão Geral")
        df_prod = get_produtos_df()
        
        if not df_prod.empty:
            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Produtos", len(df_prod))
            col1.metric("Itens em Estoque", df_prod['quantidade'].sum())
            
            valor_total = (df_prod['quantidade'] * df_prod['valor_unitario']).sum()
            col2.metric("Valor do Estoque", f"R$ {valor_total:,.2f}")
            
            # Alertas
            baixo_estoque = df_prod[df_prod['quantidade'] <= df_prod['estoque_minimo']]
            col3.metric("⚠ Alertas", len(baixo_estoque))
            
            st.divider()
            
            if not baixo_estoque.empty:
                st.warning("🔻 Produtos com estoque baixo:")
                st.dataframe(baixo_estoque[['nome', 'quantidade', 'estoque_minimo']], use_container_width=True)
            else:
                st.success("✅ Estoque saudável.")
        else:
            st.info("Nenhum produto cadastrado.")

    # --- 2. Consultar Estoque ---
    elif choice == "Consultar Estoque":
        st.header("🔎 Produtos")
        df = get_produtos_df()
        
        if not df.empty:
            search = st.text_input("Buscar...")
            if search:
                # Filtro insensível a maiúsculas/minúsculas
                mask = df['nome'].str.contains(search, case=False, na=False) | \
                       df['categoria'].str.contains(search, case=False, na=False)
                df = df[mask]
            
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Estoque vazio.")

    # --- 3. Registrar Movimentação ---
    elif choice == "Registrar Movimentação":
        st.header("🔄 Entrada / Saída")
        
        # Cria lista de nomes para o selectbox
        produtos_lista = st.session_state['db_produtos']
        
        if produtos_lista:
            nomes_prod = [p['nome'] for p in produtos_lista]
            nome_selecionado = st.selectbox("Selecione o Produto", nomes_prod)
            
            # Encontrar o dicionário do produto selecionado
            produto_atual = next(p for p in produtos_lista if p['nome'] == nome_selecionado)
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"Estoque Atual: **{produto_atual['quantidade']}**")
            
            with col2:
                tipo_mov = st.radio("Tipo", ["Entrada", "Saída"])
                qtd_mov = st.number_input("Quantidade", min_value=1, step=1)
            
            if st.button("Confirmar"):
                nova_qtd = produto_atual['quantidade']
                erro = False
                
                if tipo_mov == "Entrada":
                    nova_qtd += qtd_mov
                else:
                    if qtd_mov > nova_qtd:
                        st.error("Quantidade insuficiente!")
                        erro = True
                    else:
                        nova_qtd -= qtd_mov
                
                if not erro:
                    # Atualiza na lista em memória
                    produto_atual['quantidade'] = nova_qtd
                    
                    # Registra no histórico
                    st.session_state['db_movimentacoes'].append({
                        'data_hora': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'produto': produto_atual['nome'],
                        'tipo': tipo_mov,
                        'quantidade': qtd_mov,
                        'usuario': st.session_state['username']
                    })
                    
                    st.success("Movimentação registrada!")
                    time.sleep(1)
                    st.rerun()
        else:
            st.warning("Cadastre produtos primeiro.")

    # --- 4. Cadastro (Admin) ---
    elif choice == "Cadastro de Produtos":
        st.header("📝 Gerenciar Produtos")
        
        tab1, tab2 = st.tabs(["Novo", "Editar/Excluir"])
        
        with tab1:
            with st.form("novo_prod"):
                nome = st.text_input("Nome")
                cat = st.text_input("Categoria")
                val = st.number_input("Valor", min_value=0.01)
                desc = st.text_area("Descrição")
                colA, colB = st.columns(2)
                qtd = colA.number_input("Qtd Inicial", min_value=0)
                min_est = colB.number_input("Estoque Mínimo", value=5)
                
                if st.form_submit_button("Salvar"):
                    novo_id = st.session_state['next_prod_id']
                    st.session_state['db_produtos'].append({
                        'id': novo_id,
                        'nome': nome,
                        'categoria': cat,
                        'descricao': desc,
                        'quantidade': qtd,
                        'estoque_minimo': min_est,
                        'valor_unitario': val
                    })
                    st.session_state['next_prod_id'] += 1
                    st.success("Produto adicionado!")
                    time.sleep(0.5)
                    st.rerun()

        with tab2:
            produtos = st.session_state['db_produtos']
            if produtos:
                nomes = [p['nome'] for p in produtos]
                selecionado = st.selectbox("Selecione para editar", nomes)
                
                # Pega referência do objeto na lista
                idx, prod_obj = next(((i, p) for i, p in enumerate(produtos) if p['nome'] == selecionado), (None, None))
                
                if prod_obj:
                    with st.form("edit_prod"):
                        e_nome = st.text_input("Nome", prod_obj['nome'])
                        e_cat = st.text_input("Categoria", prod_obj['categoria'])
                        e_val = st.number_input("Valor", value=prod_obj['valor_unitario'])
                        e_min = st.number_input("Estoque Mínimo", value=prod_obj['estoque_minimo'])
                        
                        if st.form_submit_button("Atualizar"):
                            # Atualiza direto no objeto da lista
                            prod_obj['nome'] = e_nome
                            prod_obj['categoria'] = e_cat
                            prod_obj['valor_unitario'] = e_val
                            prod_obj['estoque_minimo'] = e_min
                            st.success("Atualizado!")
                            time.sleep(0.5)
                            st.rerun()
                    
                    if st.button("Excluir Produto"):
                        st.session_state['db_produtos'].pop(idx)
                        st.warning("Produto removido.")
                        time.sleep(0.5)
                        st.rerun()

    # --- 5. Histórico (Admin) ---
    elif choice == "Histórico Completo":
        st.header("📜 Log")
        df_log = get_movimentacoes_df()
        # Inverter ordem para mostrar mais recente primeiro
        if not df_log.empty:
            st.dataframe(df_log.iloc[::-1], use_container_width=True)
        else:
            st.info("Sem movimentações.")

    # --- Sair ---
    elif choice == "Sair":
        logout()