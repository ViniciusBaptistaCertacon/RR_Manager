import time

import streamlit as st
import requests
import pandas as pd
import plotly.express as px



def extrair_projeto(task):
    if "custom_fields" in task and isinstance(task["custom_fields"], dict):
        projeto = task["custom_fields"].get("custom_259")
        if projeto and isinstance(projeto, dict) and "label" in projeto:
            return projeto["label"]
    return "SEM_PROJETO_APONTADO"

def main():
    st.set_page_config(page_title="Dashboard Runrun.it", layout="wide")
    st.title("🔥 Painel do Apocalipse - Runrun.it Tarefas")
    st.caption("Você xinga, eu codifico. Incrível parceria.")

    tasks = get_tasks()
    if not tasks:
        st.warning("Não achei nada. Nem sua dignidade por sinal.")
        return

    df = pd.DataFrame(tasks)
    df["project"] = df.apply(extrair_projeto, axis=1)

    st.subheader("🧾 Lista de Tarefas")
    cols_exibicao = [col for col in ["title", "responsible_name", "task_status_name", "project", "type_name"] if col in df.columns]
    st.dataframe(df[cols_exibicao])

    st.markdown("---")
    st.subheader("📊 Gráficos Analíticos Interativos")

    col1, col2 = st.columns(2)
    with col1:
        if "task_status_name" in df.columns:
            df_status = df["task_status_name"].value_counts().reset_index()
            df_status.columns = ["task_status_name", "count"]
            fig_status = px.bar(
                df_status,
                x="task_status_name",
                y="count",
                title="Quantidade de Tarefas por Status",
                labels={"task_status_name": "Status", "count": "Quantidade"},
                text="count",
                template="plotly_white"
            )
            fig_status.update_traces(texttemplate='%{text}', textposition='outside')
            st.plotly_chart(fig_status, use_container_width=True)
        else:
            st.text("Nenhum status encontrado. É o caos mesmo.")

    with col2:
        if "responsible_name" in df.columns:
            df_resp = df["responsible_name"].value_counts().reset_index()
            df_resp.columns = ["responsible_name", "count"]
            fig_resp = px.bar(
                df_resp,
                x="responsible_name",
                y="count",
                title="Tarefas por Responsável",
                labels={"responsible_name": "Responsável", "count": "Quantidade"},
                text="count",
                template="plotly_white"
            )
            fig_resp.update_traces(texttemplate='%{text}', textposition='outside')
            st.plotly_chart(fig_resp, use_container_width=True)
        else:
            st.text("Responsáveis não encontrados. Igual seu suporte técnico.")

    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        df_proj = df["project"].value_counts().reset_index()
        df_proj.columns = ["project", "count"]
        fig_proj = px.bar(
            df_proj,
            x="project",
            y="count",
            title="Tarefas por Projeto",
            labels={"project": "Projeto", "count": "Quantidade"},
            text="count",
            template="plotly_white"
        )
        fig_proj.update_traces(texttemplate='%{text}', textposition='outside')
        st.plotly_chart(fig_proj, use_container_width=True)

    with col4:
        if "type_name" in df.columns:
            df_tipo = df["type_name"].value_counts().reset_index()
            df_tipo.columns = ["type_name", "count"]
            fig_tipo = px.bar(
                df_tipo,
                x="type_name",
                y="count",
                title="Tarefas por Tipo",
                labels={"type_name": "Tipo", "count": "Quantidade"},
                text="count",
                template="plotly_white"
            )
            fig_tipo.update_traces(texttemplate='%{text}', textposition='outside')
            st.plotly_chart(fig_tipo, use_container_width=True)
        else:
            st.text("Nenhum tipo definido. Vamos repensar essa estratégia.")

if __name__ == "__main__":
    main()
