:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: {.md-main role="main" md-component="main"}
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: {.md-main__inner .md-grid}
::::: {.md-sidebar .md-sidebar--primary md-component="sidebar" md-type="navigation"}
:::: md-sidebar__scrollwrap
::: md-sidebar__inner
[![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEyIDhhMyAzIDAgMCAwIDMtMyAzIDMgMCAwIDAtMy0zIDMgMyAwIDAgMC0zIDMgMyAzIDAgMCAwIDMgM20wIDMuNTRDOS42NCA5LjM1IDYuNSA4IDMgOHYxMWMzLjUgMCA2LjY0IDEuMzUgOSAzLjU0IDIuMzYtMi4xOSA1LjUtMy41NCA5LTMuNTRWOGMtMy41IDAtNi42NCAxLjM1LTkgMy41NCIgLz48L3N2Zz4=)](.. "Projeto BlackOps - Docs"){.md-nav__button
.md-logo aria-label="Projeto BlackOps - Docs" md-component="logo"}
Projeto BlackOps - Docs

[[ Início ]{.md-ellipsis}](..){.md-nav__link}

[[ Interface Streamlit ]{.md-ellipsis}](../ui/){.md-nav__link}

[ Referência Técnica ]{.md-ellipsis} []{.md-nav__icon .md-icon}

[]{.md-nav__icon .md-icon} Referência Técnica

- [[ Módulo App
  ]{.md-ellipsis}](../modules/app_interface/){.md-nav__link}
- [[ Módulo Blackops
  ]{.md-ellipsis}](../modules/blackops_interface/){.md-nav__link}

[ Referência ]{.md-ellipsis} []{.md-nav__icon .md-icon} [[ Referência
]{.md-ellipsis}](./){.md-nav__link .md-nav__link--active}

[]{.md-nav__icon .md-icon} Índice

- [[ github_dashboard
  ]{.md-ellipsis}](#dashboard.github_dashboard){.md-nav__link}
- [[ GitHubDashboard
  ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard){.md-nav__link}
  - [[ decodificar_resposta
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.decodificar_resposta){.md-nav__link}
  - [[ detectar_porta_serial
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.detectar_porta_serial){.md-nav__link}
  - [[ enviar_comando
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.enviar_comando){.md-nav__link}
  - [[ exibir_analise_xor
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_analise_xor){.md-nav__link}
  - [[ exibir_data_science
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_data_science){.md-nav__link}
  - [[ exibir_data_science_plot
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_data_science_plot){.md-nav__link}
  - [[ exibir_data_science_resumo
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_data_science_resumo){.md-nav__link}
  - [[ exibir_lista_repositorios
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_lista_repositorios){.md-nav__link}
  - [[ exibir_perfil
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_perfil){.md-nav__link}
  - [[ exibir_relay_firewall
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_relay_firewall){.md-nav__link}
  - [[ exibir_repositorios
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_repositorios){.md-nav__link}
  - [[ exibir_repositorios_publicos
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_repositorios_publicos){.md-nav__link}
  - [[ exibir_resultado
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_resultado){.md-nav__link}
  - [[ exibir_series_temporais
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_series_temporais){.md-nav__link}
  - [[ show_dashboard
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.show_dashboard){.md-nav__link}
- [[ streamlit_interface
  ]{.md-ellipsis}](#blackops.ui.streamlit_interface){.md-nav__link}
- [[ executar_funcao
  ]{.md-ellipsis}](#blackops.ui.streamlit_interface.executar_funcao){.md-nav__link}
- [[ load_config
  ]{.md-ellipsis}](#blackops.ui.streamlit_interface.load_config){.md-nav__link}
- [[ show_comandos_disponiveis
  ]{.md-ellipsis}](#blackops.ui.streamlit_interface.show_comandos_disponiveis){.md-nav__link}
- [[ show_project_info
  ]{.md-ellipsis}](#blackops.ui.streamlit_interface.show_project_info){.md-nav__link}
:::
::::
:::::

::::: {.md-sidebar .md-sidebar--secondary md-component="sidebar" md-type="toc"}
:::: md-sidebar__scrollwrap
::: md-sidebar__inner
[]{.md-nav__icon .md-icon} Índice

- [[ github_dashboard
  ]{.md-ellipsis}](#dashboard.github_dashboard){.md-nav__link}
- [[ GitHubDashboard
  ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard){.md-nav__link}
  - [[ decodificar_resposta
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.decodificar_resposta){.md-nav__link}
  - [[ detectar_porta_serial
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.detectar_porta_serial){.md-nav__link}
  - [[ enviar_comando
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.enviar_comando){.md-nav__link}
  - [[ exibir_analise_xor
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_analise_xor){.md-nav__link}
  - [[ exibir_data_science
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_data_science){.md-nav__link}
  - [[ exibir_data_science_plot
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_data_science_plot){.md-nav__link}
  - [[ exibir_data_science_resumo
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_data_science_resumo){.md-nav__link}
  - [[ exibir_lista_repositorios
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_lista_repositorios){.md-nav__link}
  - [[ exibir_perfil
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_perfil){.md-nav__link}
  - [[ exibir_relay_firewall
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_relay_firewall){.md-nav__link}
  - [[ exibir_repositorios
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_repositorios){.md-nav__link}
  - [[ exibir_repositorios_publicos
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_repositorios_publicos){.md-nav__link}
  - [[ exibir_resultado
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_resultado){.md-nav__link}
  - [[ exibir_series_temporais
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.exibir_series_temporais){.md-nav__link}
  - [[ show_dashboard
    ]{.md-ellipsis}](#dashboard.github_dashboard.GitHubDashboard.show_dashboard){.md-nav__link}
- [[ streamlit_interface
  ]{.md-ellipsis}](#blackops.ui.streamlit_interface){.md-nav__link}
- [[ executar_funcao
  ]{.md-ellipsis}](#blackops.ui.streamlit_interface.executar_funcao){.md-nav__link}
- [[ load_config
  ]{.md-ellipsis}](#blackops.ui.streamlit_interface.load_config){.md-nav__link}
- [[ show_comandos_disponiveis
  ]{.md-ellipsis}](#blackops.ui.streamlit_interface.show_comandos_disponiveis){.md-nav__link}
- [[ show_project_info
  ]{.md-ellipsis}](#blackops.ui.streamlit_interface.show_project_info){.md-nav__link}
:::
::::
:::::

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: {.md-content md-component="content"}
# Referência da Interface {#referencia-da-interface}

:::::::::::::::::::::::::::::::::::::::::::::::::::::: {.doc .doc-object .doc-module}
[]{#dashboard.github_dashboard}

::::::::::::::::::::::::::::::::::::::::::::::::::::: {.doc .doc-contents .first}
:::::::::::::::::::::::::::::::::::::::::::::::::::: {.doc .doc-children}
::::::::::::::::::::::::::::::::::::::::::::::::::: {.doc .doc-object .doc-class}
## `GitHubDashboard` {#dashboard.github_dashboard.GitHubDashboard .doc .doc-heading}

:::::::::::::::::::::::::::::::::::::::::::::::::: {.doc .doc-contents}
Source code in `dashboard\github_dashboard.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|      12                           |                                   |
|      13                           |     class GitHubDashboard:        |
|      14                           |                                   |
|      15                           |    def __init__(self, user_data): |
|      16                           |                                   |
|      17                           |        self.user_data = user_data |
|      18                           |                                   |
|      19                           |                                   |
|      20                           | def show_dashboard(self) -> None: |
|      21                           |             """                   |
|      22                           |             Exibe a lista         |
|      23                           | de funcionalidades no aplicative. |
|      24                           |                                   |
|      25                           |             Returns:              |
|      26                           |                                   |
|      27                           |             Show (None): Configur |
|      28                           | ações carregadas do arquivo YAML. |
|      29                           |             """                   |
|      30                           |             tabs = st.tabs([      |
|      31                           |                 "👤 Perfil",      |
|      32                           |                                   |
|      33                           |       "📦 Repositórios Públicos", |
|      34                           |                                   |
|      35                           |              "🗃️ Lista Detalhada", |
|      36                           |                                   |
|      37                           |            "📊 Regressão - Info", |
|      38                           |                                   |
|      39                           |         "📉 Regressão - Gráfico", |
|      40                           |                                   |
|      41                           |              "🛡️ Relay e Firewall" |
|      42                           |             ])                    |
|      43                           |                                   |
|      44                           |             with tabs[0]:         |
|      45                           |                                   |
|      46                           |              self.exibir_perfil() |
|      47                           |                                   |
|      48                           |             with tabs[1]:         |
|      49                           |                 se                |
|      50                           | lf.exibir_repositorios_publicos() |
|      51                           |                                   |
|      52                           |             with tabs[2]:         |
|      53                           |                                   |
|      54                           |  self.exibir_lista_repositorios() |
|      55                           |                                   |
|      56                           |             with tabs[3]:         |
|      57                           |                                   |
|      58                           |        self.exibir_data_science() |
|      59                           |                                   |
|      60                           |             with tabs[4]:         |
|      61                           |                                   |
|      62                           |   self.exibir_data_science_plot() |
|      63                           |                                   |
|      64                           |             with tabs[5]:         |
|      65                           |                                   |
|      66                           |      self.exibir_relay_firewall() |
|      67                           |                                   |
|      68                           |                                   |
|      69                           |  def exibir_perfil(self) -> None: |
|      70                           |             """                   |
|      71                           |             Exi                   |
|      72                           | be o perfil do usuário do github. |
|      73                           |                                   |
|      74                           |             Returns:              |
|      75                           |                                   |
|      76                           |           Exibir (None): Configur |
|      77                           | ações carregadas do arquivo YAML. |
|      78                           |             """                   |
|      79                           |                                   |
|      80                           |   st.title("👤 GitHub Dashboard") |
|      81                           |                                   |
|      82                           |   col1, col2 = st.columns([1, 3]) |
|      83                           |             with col1:            |
|      84                           |                                   |
|      85                           |              st.image(self.user_d |
|      86                           | ata.get("avatar_url"), width=120) |
|      87                           |             with col2:            |
|      88                           |                 st.su             |
|      89                           | bheader(self.user_data.get("name" |
|      90                           | ) or self.user_data.get("login")) |
|      91                           |                 st.caption(f"[🔗  |
|      92                           | {self.user_data.get('login')}]({s |
|      93                           | elf.user_data.get('html_url')})") |
|      94                           |                 i                 |
|      95                           | f self.user_data.get("location"): |
|      96                           |                     st.text(f"    |
|      97                           | 📍 {self.user_data['location']}") |
|      98                           |                                   |
|      99                           |   if self.user_data.get("email"): |
|     100                           |                     st.text       |
|     101                           | (f"📧 {self.user_data['email']}") |
|     102                           |                                   |
|     103                           |     if self.user_data.get("bio"): |
|     104                           |                     st.markdow    |
|     105                           | n(f"> _{self.user_data['bio']}_") |
|     106                           |                                   |
|     107                           |         def e                     |
|     108                           | xibir_repositorios(self) -> None: |
|     109                           |             """                   |
|     110                           |             Exibe a lis           |
|     111                           | ta de repositórios no aplicative. |
|     112                           |                                   |
|     113                           |             Returns:              |
|     114                           |                                   |
|     115                           |             Show (None): Configur |
|     116                           | ações carregadas do arquivo YAML. |
|     117                           |             """                   |
|     118                           |             aba1, aba2 = st.tabs( |
|     119                           | ["📦 Repositórios Públicos", "🗃️ L |
|     120                           | ista Detalhada de Repositórios"]) |
|     121                           |             with aba1:            |
|     122                           |                 se                |
|     123                           | lf.exibir_repositorios_publicos() |
|     124                           |             with aba2:            |
|     125                           |                                   |
|     126                           |  self.exibir_lista_repositorios() |
|     127                           |                                   |
|     128                           |         def exibir_rep            |
|     129                           | ositorios_publicos(self) -> None: |
|     130                           |             """                   |
|     131                           |             Exibe a lista de rep  |
|     132                           | ositórios publicos no aplicative. |
|     133                           |                                   |
|     134                           |             Returns:              |
|     135                           |                                   |
|     136                           |             Show (None): Configur |
|     137                           | ações carregadas do arquivo YAML. |
|     138                           |             """                   |
|     139                           |             st.subh               |
|     140                           | eader("📦 Repositórios Públicos") |
|     141                           |             repos_url             |
|     142                           | = self.user_data.get("repos_url") |
|     143                           |             if repos_url:         |
|     144                           |                 r                 |
|     145                           | esponse = requests.get(repos_url) |
|     146                           |                                   |
|     147                           |   if response.status_code == 200: |
|     148                           |                                   |
|     149                           |           repos = response.json() |
|     150                           |                                   |
|     151                           |       if isinstance(repos, list): |
|     152                           |                                   |
|     153                           |          for repo in repos[:100]: |
|     154                           |                                   |
|     155                           |             st.markdown(f"📔️ [{re |
|     156                           | po['name']}]({repo['html_url']})  |
|     157                           | — ⭐ {repo['stargazers_count']}") |
|     158                           |                     else:         |
|     159                           |                                   |
|     160                           |                        st.warning |
|     161                           | ("\u26a0\ufe0f Dados de repositór |
|     162                           | ios inválidos recebidos da API.") |
|     163                           |                 else:             |
|     164                           |                     st            |
|     165                           | .error(f"❌ Erro ao acessar repos |
|     166                           | itórios: {response.status_code}") |
|     167                           |                                   |
|     168                           |         def exibir_               |
|     169                           | lista_repositorios(self) -> None: |
|     170                           |             """                   |
|     171                           |                                   |
|     172                           |            Exibe a lista de repos |
|     173                           | itórios detalhados no aplicative. |
|     174                           |                                   |
|     175                           |             Returns:              |
|     176                           |                                   |
|     177                           |             Show (None): Configur |
|     178                           | ações carregadas do arquivo YAML. |
|     179                           |             """                   |
|     180                           |             st.subheader("📃      |
|     181                           | Lista Detalhada de Repositórios") |
|     182                           |             repos_url             |
|     183                           | = self.user_data.get("repos_url") |
|     184                           |             if repos_url:         |
|     185                           |                 try:              |
|     186                           |                     repos         |
|     187                           |  = requests.get(repos_url).json() |
|     188                           |                                   |
|     189                           |        df_repos = pd.DataFrame([{ |
|     190                           |                                   |
|     191                           |             "Nome": repo["name"], |
|     192                           |                         "Descriç  |
|     193                           | ão": repo.get("description", ""), |
|     194                           |                         "Est      |
|     195                           | relas": repo["stargazers_count"], |
|     196                           |                                   |
|     197                           |     "Forks": repo["forks_count"], |
|     198                           |                                   |
|     199                           |          "URL": repo["html_url"], |
|     200                           |                         "Linguag  |
|     201                           | em": repo.get("language", "N/A"), |
|     202                           |                         "A        |
|     203                           | tualizado em": repo["updated_at"] |
|     204                           |                                   |
|     205                           |             } for repo in repos]) |
|     206                           |                                   |
|     207                           |            st.dataframe(df_repos) |
|     208                           |                                   |
|     209                           |            except Exception as e: |
|     210                           |                                   |
|     211                           |                    st.error(f"Err |
|     212                           | o ao carregar repositórios: {e}") |
|     213                           |             else:                 |
|     214                           |                 st.warning("URL   |
|     215                           | de repositórios não encontrada.") |
|     216                           |                                   |
|     217                           |         def e                     |
|     218                           | xibir_data_science(self) -> None: |
|     219                           |             """                   |
|     220                           |             Exibe a lista de m    |
|     221                           | étodos datascience no aplicative. |
|     222                           |                                   |
|     223                           |             Returns:              |
|     224                           |                                   |
|     225                           |             Show (None): Configur |
|     226                           | ações carregadas do arquivo YAML. |
|     227                           |             """                   |
|     228                           |                                   |
|     229                           |      aba1, aba2, aba3 = st.tabs([ |
|     230                           |                 "📈 Data S        |
|     231                           | cience: Regression Table - Info", |
|     232                           |                 "📈 Data S        |
|     233                           | cience: Regression Table - Plot", |
|     234                           |                 "📊               |
|     235                           |  Data Science: Séries Temporais"  |
|     236                           |             ])                    |
|     237                           |             with aba1:            |
|     238                           |                                   |
|     239                           | self.exibir_data_science_resumo() |
|     240                           |             with aba2:            |
|     241                           |                                   |
|     242                           |   self.exibir_data_science_plot() |
|     243                           |             with aba3:            |
|     244                           |                                   |
|     245                           |    self.exibir_series_temporais() |
|     246                           |                                   |
|     247                           |         def exibir_d              |
|     248                           | ata_science_resumo(self) -> None: |
|     249                           |             """                   |
|     250                           |             Método DataScience.   |
|     251                           |                                   |
|     252                           |             Returns:              |
|     253                           |                                   |
|     254                           |           Show (Resumo): Configur |
|     255                           | ações carregadas do arquivo YAML. |
|     256                           |             """                   |
|     257                           |                                   |
|     258                           |           st.subheader("📈 Data S |
|     259                           | cience: Regression Table - Info") |
|     260                           |             try:                  |
|     261                           |                 linguagem =       |
|     262                           | self.user_data.get("language", 0) |
|     263                           |                 repos = self      |
|     264                           | .user_data.get("public_repos", 0) |
|     265                           |                                   |
|     266                           |               df = pd.DataFrame({ |
|     267                           |                                   |
|     268                           |               "linguagens": [ling |
|     269                           | uagem + i for i in range(-5, 5)], |
|     270                           |                                   |
|     271                           |                  "repositorios":  |
|     272                           | [repos + i for i in range(-5, 5)] |
|     273                           |                 })                |
|     274                           |                                   |
|     275                           |              X = df["linguagens"] |
|     276                           |                                   |
|     277                           |            y = df["repositorios"] |
|     278                           |                                   |
|     279                           |      X_const = sm.add_constant(X) |
|     280                           |                                   |
|     281                           | modelo = sm.OLS(y, X_const).fit() |
|     282                           |                 st                |
|     283                           | .write("**Resumo da Regressão Lin |
|     284                           | ear com seus dados do GitHub:**") |
|     285                           |                                   |
|     286                           |         st.text(modelo.summary()) |
|     287                           |                                   |
|     288                           |            except Exception as e: |
|     289                           |                 st.error(         |
|     290                           | f"Erro ao exibir regressão: {e}") |
|     291                           |                                   |
|     292                           |         def exibir                |
|     293                           | _data_science_plot(self) -> None: |
|     294                           |             """                   |
|     295                           |             Método DataScience.   |
|     296                           |                                   |
|     297                           |             Returns:              |
|     298                           |                                   |
|     299                           |             Show (Plot): Configur |
|     300                           | ações carregadas do arquivo YAML. |
|     301                           |             """                   |
|     302                           |                                   |
|     303                           |           st.subheader("📈 Data S |
|     304                           | cience: Regression Table - Plot") |
|     305                           |             try:                  |
|     306                           |                 linguagem =       |
|     307                           | self.user_data.get("language", 0) |
|     308                           |                 repos = self      |
|     309                           | .user_data.get("public_repos", 0) |
|     310                           |                                   |
|     311                           |               df = pd.DataFrame({ |
|     312                           |                                   |
|     313                           |               "linguagens": [ling |
|     314                           | uagem + i for i in range(-5, 5)], |
|     315                           |                                   |
|     316                           |                  "repositorios":  |
|     317                           | [repos + i for i in range(-5, 5)] |
|     318                           |                 })                |
|     319                           |                                   |
|     320                           |          fig, ax = plt.subplots() |
|     321                           |                                   |
|     322                           |      sns.regplot(x="linguagens",  |
|     323                           | y="repositorios", data=df, ax=ax) |
|     324                           |                                   |
|     325                           |                ax.set_title("Regr |
|     326                           | essão Linear: Linguagens vs Repos |
|     327                           | itórios (Baseada no seu GitHub)") |
|     328                           |                 st.pyplot(fig)    |
|     329                           |                                   |
|     330                           |            except Exception as e: |
|     331                           |                                   |
|     332                           |              st.error(f"Erro ao e |
|     333                           | xibir gráfico de regressão: {e}") |
|     334                           |                                   |
|     335                           |         def exibi                 |
|     336                           | r_series_temporais(self) -> None: |
|     337                           |             """                   |
|     338                           |             Método DataScience.   |
|     339                           |                                   |
|     340                           |             Returns:              |
|     341                           |                                   |
|     342                           |        Show (Temporais): Configur |
|     343                           | ações carregadas do arquivo YAML. |
|     344                           |             """                   |
|     345                           |             st.su                 |
|     346                           | bheader("📊 Análise de Séries Tem |
|     347                           | porais com seus dados do GitHub") |
|     348                           |             try:                  |
|     349                           |                                   |
|     350                           |                # Simula evolução  |
|     351                           | de repositórios com base no tempo |
|     352                           |                 linguagem =       |
|     353                           | self.user_data.get("language", 0) |
|     354                           |                 repos = self      |
|     355                           | .user_data.get("public_repos", 0) |
|     356                           |                                   |
|     357                           |        datas = pd.date_range(end= |
|     358                           | pd.Timestamp.today(), periods=10) |
|     359                           |                                   |
|     360                           |                                   |
|     361                           |               df = pd.DataFrame({ |
|     362                           |                                   |
|     363                           |                    "data": datas, |
|     364                           |                                   |
|     365                           |                  "linguagens": [l |
|     366                           | inguagem + i for i in range(10)], |
|     367                           |                                   |
|     368                           |       "repositorios": [repos + i  |
|     369                           | + (i % 3 - 1) for i in range(10)] |
|     370                           |                                   |
|     371                           |              }).set_index("data") |
|     372                           |                                   |
|     373                           |                                   |
|     374                           |        # Gráfico de linha simples |
|     375                           |                 st                |
|     376                           | .line_chart(df[["repositorios"]]) |
|     377                           |                                   |
|     378                           |                 # Média móvel     |
|     379                           |                                   |
|     380                           |    df["media_movel"] = df["reposi |
|     381                           | torios"].rolling(window=3).mean() |
|     382                           |                                   |
|     383                           |          fig, ax = plt.subplots() |
|     384                           |                                   |
|     385                           |   df["repositorios"].plot(ax=ax,  |
|     386                           | label="Repositórios", marker="o") |
|     387                           |                 df["media         |
|     388                           | _movel"].plot(ax=ax, label="Média |
|     389                           |  Móvel (3 dias)", linestyle="--") |
|     390                           |                 ax                |
|     391                           | .set_title("Repositórios GitHub - |
|     392                           |  Série Temporal com Média Móvel") |
|     393                           |                 ax.legend()       |
|     394                           |                 st.pyplot(fig)    |
|     395                           |                                   |
|     396                           |                                   |
|     397                           |            except Exception as e: |
|     398                           |                 st.error(f"Erro   |
|     399                           | ao exibir séries temporais: {e}") |
|     400                           |                                   |
|     401                           |                                   |
|     402                           |         def exi                   |
|     403                           | bir_relay_firewall(self) -> None: |
|     404                           |             """                   |
|     405                           |                                   |
|     406                           |    Exibe as informações do relay. |
|     407                           |                                   |
|     408                           |             Returns:              |
|     409                           |                                   |
|     410                           |            Show (Relay): Configur |
|     411                           | ações carregadas do arquivo YAML. |
| :::                               |             """                   |
|                                   |             log = []              |
|                                   |                                   |
|                                   |             st.subheader("🚀 C    |
|                                   | ibersegurança: Relay e Firewall") |
|                                   |             status = st.empty()   |
|                                   |             reiniciar             |
|                                   |  = st.button("💡 Reiniciar Relé") |
|                                   |                                   |
|                                   |             porta_serial = self.  |
|                                   | detectar_porta_serial() or "COM4" |
|                                   |             baud_rate = 9600      |
|                                   |                                   |
|                                   |             try:                  |
|                                   |                 if reiniciar:     |
|                                   |                                   |
|                                   |   st.write("Reiniciando relé...") |
|                                   |                     log           |
|                                   | = ["✅ Comando enviado: RESTART"] |
|                                   |                                   |
|                                   |    self.enviar_comando(porta_seri |
|                                   | al, baud_rate, b"RESTART\n", log) |
|                                   |                                   |
|                                   |                  status.success(" |
|                                   | Relé Reiniciado com sucesso! ✅") |
|                                   |                                   |
|                                   |                 st.inf            |
|                                   | o(f"🔌 Iniciando comunicação seri |
|                                   | al na porta `{porta_serial}`...") |
|                                   |                                   |
|                                   |     with serial.Serial(porta_seri |
|                                   | al, baud_rate, timeout=2) as ser: |
|                                   |                     time.sleep(2) |
|                                   |                                   |
|                                   |          ser.write(b"FIREWALL\n") |
|                                   |                     log =         |
|                                   |  ["✅ Comando enviado: FIREWALL"] |
|                                   |                                   |
|                                   |               start = time.time() |
|                                   |                                   |
|                                   |     raw_response = ser.readline() |
|                                   |                                   |
|                                   |    latencia = time.time() - start |
|                                   |                                   |
|                                   |                 if log:           |
|                                   |                                   |
|                                   |                 self.exibir_resul |
|                                   | tado(raw_response, latencia, log) |
|                                   |                                   |
|                                   |             exc                   |
|                                   | ept serial.SerialException as se: |
|                                   |                 st.error          |
|                                   | (f"Erro de conexão serial: {se}") |
|                                   |                                   |
|                                   |            except Exception as e: |
|                                   |                                   |
|                                   | st.error(f"Erro inesperado: {e}") |
|                                   |                                   |
|                                   |         def det                   |
|                                   | ectar_porta_serial(self) -> None: |
|                                   |             """                   |
|                                   |             Método de detecç      |
|                                   | ão da porta serial do aplicativo. |
|                                   |                                   |
|                                   |             Returns:              |
|                                   |                                   |
|                                   |             Show (Port): Configur |
|                                   | ações carregadas do arquivo YAML. |
|                                   |             """                   |
|                                   |             portas = list(se      |
|                                   | rial.tools.list_ports.comports()) |
|                                   |             for p in portas:      |
|                                   |                 if a              |
|                                   | ny(chave in p.description for cha |
|                                   | ve in ["USB", "CH340", "CP210"]): |
|                                   |                                   |
|                                   |                   return p.device |
|                                   |             return None           |
|                                   |                                   |
|                                   |         def enviar_comando(self,  |
|                                   |  porta, baud_rate, comando, log): |
|                                   |             """                   |
|                                   |             Método que exec       |
|                                   | uta a operação de enviar comando. |
|                                   |                                   |
|                                   |             Returns:              |
|                                   |                                   |
|                                   |          Send (Command): Configur |
|                                   | ações carregadas do arquivo YAML. |
|                                   |             """                   |
|                                   |             try:                  |
|                                   |                                   |
|                                   |            with serial.Serial(por |
|                                   | ta, baud_rate, timeout=1) as ser: |
|                                   |                                   |
|                                   |      if isinstance(comando, str): |
|                                   |                                   |
|                                   |        comando = comando.encode() |
|                                   |                                   |
|                                   |                ser.write(comando) |
|                                   |                     log.a         |
|                                   | ppend(f"✅ Comando enviado (inter |
|                                   | no): {comando.decode().strip()}") |
|                                   |             ex                    |
|                                   | cept serial.SerialException as e: |
|                                   |                 log.              |
|                                   | append(f"❌ Erro ao enviar comand |
|                                   | o para a porta serial: {str(e)}") |
|                                   |                                   |
|                                   |            except Exception as e: |
|                                   |                 log.append        |
|                                   | (f"❌ Erro inesperado: {str(e)}") |
|                                   |                                   |
|                                   |                                   |
|                                   |   def exibir_resultado(self, raw_ |
|                                   | response, latencia, log) -> None: |
|                                   |             """                   |
|                                   |             Exibe o re            |
|                                   | sultado das informações do relay. |
|                                   |                                   |
|                                   |             Returns:              |
|                                   |                                   |
|                                   |            Show (Relay): Configur |
|                                   | ações carregadas do arquivo YAML. |
|                                   |             """                   |
|                                   |                                   |
|                                   |        response_str = self.decodi |
|                                   | ficar_resposta(raw_response, log) |
|                                   |                                   |
|                                   |  abas = st.tabs(["📱 Resposta", " |
|                                   | 📦 Bytes Recebidos", "🧾 Log de D |
|                                   | ecodificação", "🧪 Análise XOR"]) |
|                                   |                                   |
|                                   |             with abas[0]:         |
|                                   |                 st.subhea         |
|                                   | der("📱 Resposta do Dispositivo") |
|                                   |                 if response_str:  |
|                                   |                                   |
|                                   |          st.success(f"📱 Resposta |
|                                   |  do dispositivo: {response_str}") |
|                                   |                 else:             |
|                                   |                     st.warning("  |
|                                   | ⚠️ Dados não textuais recebidos.") |
|                                   |                     st.code(raw   |
|                                   | _response.hex(), language="text") |
|                                   |                                   |
|                                   |                                   |
|                                   |           st.text(f"⏱️ Tempo de re |
|                                   | sposta: {latencia:.2f} segundos") |
|                                   |                                   |
|                                   |                 if response_str   |
|                                   | and "OK" in response_str.upper(): |
|                                   |                                   |
|                                   |                 st.success("🔍 Fi |
|                                   | rewall validado e relay seguro.") |
|                                   |                                   |
|                                   |                elif response_str: |
|                                   |                     st.warning(f" |
|                                   | ❗ Resposta inesperada: '{respons |
|                                   | e_str}' — verifique o firmware.") |
|                                   |                 else:             |
|                                   |                                   |
|                                   |           st.error("❌ Nenhuma re |
|                                   | sposta válida foi interpretada.") |
|                                   |                                   |
|                                   |             with abas[1]:         |
|                                   |                 st                |
|                                   | .code(" ".join(f"{b:02x}" for b i |
|                                   | n raw_response), language="text") |
|                                   |                                   |
|                                   |       byte_table = pd.DataFrame({ |
|                                   |                                   |
|                                   |                  "Byte (Hex)": [f |
|                                   | "{b:02x}" for b in raw_response], |
|                                   |                     "Byte (Dec)"  |
|                                   | : [str(b) for b in raw_response], |
|                                   |                                   |
|                                   | "ASCII": [chr(b) if 32 <= b <= 12 |
|                                   | 6 else "." for b in raw_response] |
|                                   |                 })                |
|                                   |                 with s            |
|                                   | t.expander("📦 Bytes Recebidos"): |
|                                   |                                   |
|                                   |          st.dataframe(byte_table) |
|                                   |                                   |
|                                   |             with abas[2]:         |
|                                   |                 st.sub            |
|                                   | header("🧾 Log de Decodificação") |
|                                   |                 st.code           |
|                                   | ("\n".join(log), language="text") |
|                                   |                                   |
|                                   |             with abas[3]:         |
|                                   |                 self              |
|                                   | .exibir_analise_xor(raw_response) |
|                                   |                                   |
|                                   |         def decodificar_          |
|                                   | resposta(self, raw, log) -> None: |
|                                   |             """                   |
|                                   |                                   |
|                                   |        Método de descriptografia. |
|                                   |                                   |
|                                   |             Returns:              |
|                                   |                                   |
|                                   |         Show (Descript): Configur |
|                                   | ações carregadas do arquivo YAML. |
|                                   |             """                   |
|                                   |             try:                  |
|                                   |                                   |
|                                   |    response = raw.decode("utf-8") |
|                                   |                 log.              |
|                                   | append("🔍 Decodificação: UTF-8") |
|                                   |                 return response   |
|                                   |                                   |
|                                   |        except UnicodeDecodeError: |
|                                   |                 try:              |
|                                   |                                   |
|                                   |   response = raw.decode("latin1") |
|                                   |                     log.ap        |
|                                   | pend("🔍 Decodificação: Latin-1") |
|                                   |                                   |
|                                   |                   return response |
|                                   |                 except Exception: |
|                                   |                     try:          |
|                                   |                                   |
|                                   |                  base64_str = raw |
|                                   | .decode("utf-8", errors="ignore") |
|                                   |                         decode    |
|                                   | d = base64.b64decode(base64_str). |
|                                   | decode("utf-8", errors="replace") |
|                                   |                                   |
|                                   |                  log.append("🔍 D |
|                                   | ecodificação: Base64 (fallback)") |
|                                   |                                   |
|                                   |                    return decoded |
|                                   |                                   |
|                                   |            except Exception as e: |
|                                   |                                   |
|                                   |               log.append(f"🚨 Fal |
|                                   | ha na decodificação base64: {e}") |
|                                   |             return None           |
|                                   |                                   |
|                                   |         def exibir_analise        |
|                                   | _xor(self, raw_response) -> None: |
|                                   |             """                   |
|                                   |                                   |
|                                   |        Exibe as informações do re |
|                                   | lay, com base em uma análise XOR. |
|                                   |                                   |
|                                   |             Returns:              |
|                                   |                                   |
|                                   |              Show (Xor): Configur |
|                                   | ações carregadas do arquivo YAML. |
|                                   |             """                   |
|                                   |                                   |
|                                   |  st.subheader("🧪 Análise XOR Bru |
|                                   | te Force - Tabela Redimensional") |
|                                   |             palavras_chave = ["OK |
|                                   | ", "FIREWALL", "ACCESS", "RESTART |
|                                   | ", "DENIED", "GRANTED", "SECURE"] |
|                                   |             tabela_xor = []       |
|                                   |                                   |
|                                   |                                   |
|                                   |         for key in range(1, 256): |
|                                   |                 xor_result        |
|                                   | = [b ^ key for b in raw_response] |
|                                   |                 decode            |
|                                   | d = ''.join(chr(b) if 32 <= b <=  |
|                                   | 126 else '.' for b in xor_result) |
|                                   |                                   |
|                                   |                 palavras_detect   |
|                                   | adas = [p for p in palavras_chave |
|                                   |  if p.upper() in decoded.upper()] |
|                                   |                                   |
|                                   |   printable_chars = sum(1 for c i |
|                                   | n decoded if 32 <= ord(c) <= 126) |
|                                   |                 printable_ratio   |
|                                   |  = printable_chars / len(decoded) |
|                                   |                                   |
|                                   |                 if printable_rat  |
|                                   | io > 0.8 and palavras_detectadas: |
|                                   |                                   |
|                                   |               tabela_xor.append({ |
|                                   |                                   |
|                                   |                       "Key": key, |
|                                   |                         "P        |
|                                   | rintable Ratio": printable_ratio, |
|                                   |                                   |
|                                   |                    "Qtd Palavras- |
|                                   | chave": len(palavras_detectadas), |
|                                   |                                   |
|                                   |         "Palavra-chave Detectada" |
|                                   | : ", ".join(palavras_detectadas), |
|                                   |                                   |
|                                   |     "Texto Decodificado": decoded |
|                                   |                     })            |
|                                   |                                   |
|                                   |             if tabela_xor:        |
|                                   |                 df_xor =          |
|                                   | pd.DataFrame(tabela_xor).sort_val |
|                                   | ues(by=["Qtd Palavras-chave", "Pr |
|                                   | intable Ratio"], ascending=False) |
|                                   |                                   |
|                                   |                                   |
|                                   |     melhor_linha = df_xor.iloc[0] |
|                                   |                                   |
|                                   |    st.markdown("### 🔍 Insights") |
|                                   |                                   |
|                                   |         st.write(f"**Chave Encont |
|                                   | rada:** `{melhor_linha['Key']}`") |
|                                   |                 st.write(         |
|                                   | f"**Texto Decodificado:** `{melho |
|                                   | r_linha['Texto Decodificado']}`") |
|                                   |                                   |
|                                   |             st.write(f"**Palavras |
|                                   | -chave Detectadas:** `{melhor_lin |
|                                   | ha['Palavra-chave Detectada']}`") |
|                                   |                 st.writ           |
|                                   | e(f"**Printable Ratio:** `{melhor |
|                                   | _linha['Printable Ratio']:.2f}`") |
|                                   |                 st.write(         |
|                                   | f"**Qtd Palavras-chave:** `{melho |
|                                   | r_linha['Qtd Palavras-chave']}`") |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::

:::::::::::::::::::::::::::::::::::::::::::::::: {.doc .doc-children}
::::: {.doc .doc-object .doc-function}
### [`decodificar_resposta`{.highlight .language-python}]{.n}[`(`{.highlight .language-python}]{.p}[`raw`{.highlight .language-python}]{.n}[`,`{.highlight .language-python}]{.p}` `{.highlight .language-python}[`log`{.highlight .language-python}]{.n}[`)`{.highlight .language-python}]{.p} {#dashboard.github_dashboard.GitHubDashboard.decodificar_resposta .doc .doc-heading}

:::: {.doc .doc-contents}
Método de descriptografia.

[Returns:]{.doc-section-title}

+-----------------------+-----------------------+-----------------------+
| Name                  | Type                  | Description           |
+=======================+=======================+=======================+
| `Show`                | [`Descrip             | :                     |
|                       | t`]{title="Descript"} | :: doc-md-description |
|                       |                       | Configurações         |
|                       |                       | carregadas do arquivo |
|                       |                       | YAML.                 |
|                       |                       | :::                   |
+-----------------------+-----------------------+-----------------------+

Source code in `dashboard\github_dashboard.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|     348                           |                                   |
|     349                           |     def decodificar_              |
|     350                           | resposta(self, raw, log) -> None: |
|     351                           |         """                       |
|     352                           |                                   |
|     353                           |        Método de descriptografia. |
|     354                           |                                   |
|     355                           |         Returns:                  |
|     356                           |                                   |
|     357                           |         Show (Descript): Configur |
|     358                           | ações carregadas do arquivo YAML. |
|     359                           |         """                       |
|     360                           |         try:                      |
|     361                           |                                   |
|     362                           |    response = raw.decode("utf-8") |
|     363                           |             log.                  |
|     364                           | append("🔍 Decodificação: UTF-8") |
|     365                           |             return response       |
|     366                           |                                   |
|     367                           |        except UnicodeDecodeError: |
|     368                           |             try:                  |
|     369                           |                                   |
|     370                           |   response = raw.decode("latin1") |
|     371                           |                 log.ap            |
|     372                           | pend("🔍 Decodificação: Latin-1") |
| :::                               |                 return response   |
|                                   |             except Exception:     |
|                                   |                 try:              |
|                                   |                                   |
|                                   |                  base64_str = raw |
|                                   | .decode("utf-8", errors="ignore") |
|                                   |                     decode        |
|                                   | d = base64.b64decode(base64_str). |
|                                   | decode("utf-8", errors="replace") |
|                                   |                                   |
|                                   |                  log.append("🔍 D |
|                                   | ecodificação: Base64 (fallback)") |
|                                   |                                   |
|                                   |                    return decoded |
|                                   |                                   |
|                                   |            except Exception as e: |
|                                   |                                   |
|                                   |               log.append(f"🚨 Fal |
|                                   | ha na decodificação base64: {e}") |
|                                   |         return None               |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::
::::
:::::

::::: {.doc .doc-object .doc-function}
### [`detectar_porta_serial`{.highlight .language-python}]{.n}[`()`{.highlight .language-python}]{.p} {#dashboard.github_dashboard.GitHubDashboard.detectar_porta_serial .doc .doc-heading}

:::: {.doc .doc-contents}
Método de detecção da porta serial do aplicativo.

[Returns:]{.doc-section-title}

+-----------------------+-----------------------+-----------------------+
| Name                  | Type                  | Description           |
+=======================+=======================+=======================+
| `Show`                | [                     | :                     |
|                       | `Port`]{title="Port"} | :: doc-md-description |
|                       |                       | Configurações         |
|                       |                       | carregadas do arquivo |
|                       |                       | YAML.                 |
|                       |                       | :::                   |
+-----------------------+-----------------------+-----------------------+

Source code in `dashboard\github_dashboard.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|     273                           |                                   |
|     274                           |     def det                       |
|     275                           | ectar_porta_serial(self) -> None: |
|     276                           |         """                       |
|     277                           |         Método de detecç          |
|     278                           | ão da porta serial do aplicativo. |
|     279                           |                                   |
|     280                           |         Returns:                  |
|     281                           |             Show (Port): Configur |
|     282                           | ações carregadas do arquivo YAML. |
|     283                           |         """                       |
|     284                           |         portas = list(se          |
| :::                               | rial.tools.list_ports.comports()) |
|                                   |         for p in portas:          |
|                                   |             if a                  |
|                                   | ny(chave in p.description for cha |
|                                   | ve in ["USB", "CH340", "CP210"]): |
|                                   |                 return p.device   |
|                                   |         return None               |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::
::::
:::::

::::: {.doc .doc-object .doc-function}
### [`enviar_comando`{.highlight .language-python}]{.n}[`(`{.highlight .language-python}]{.p}[`porta`{.highlight .language-python}]{.n}[`,`{.highlight .language-python}]{.p}` `{.highlight .language-python}[`baud_rate`{.highlight .language-python}]{.n}[`,`{.highlight .language-python}]{.p}` `{.highlight .language-python}[`comando`{.highlight .language-python}]{.n}[`,`{.highlight .language-python}]{.p}` `{.highlight .language-python}[`log`{.highlight .language-python}]{.n}[`)`{.highlight .language-python}]{.p} {#dashboard.github_dashboard.GitHubDashboard.enviar_comando .doc .doc-heading}

:::: {.doc .doc-contents}
Método que executa a operação de enviar comando.

[Returns:]{.doc-section-title}

+-----------------------+-----------------------+-----------------------+
| Name                  | Type                  | Description           |
+=======================+=======================+=======================+
| `Send`                | [`Comma               | :                     |
|                       | nd`]{title="Command"} | :: doc-md-description |
|                       |                       | Configurações         |
|                       |                       | carregadas do arquivo |
|                       |                       | YAML.                 |
|                       |                       | :::                   |
+-----------------------+-----------------------+-----------------------+

Source code in `dashboard\github_dashboard.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|     286                           |                                   |
|     287                           |     def enviar_comando(self,      |
|     288                           |  porta, baud_rate, comando, log): |
|     289                           |         """                       |
|     290                           |         Método que exec           |
|     291                           | uta a operação de enviar comando. |
|     292                           |                                   |
|     293                           |         Returns:                  |
|     294                           |                                   |
|     295                           |          Send (Command): Configur |
|     296                           | ações carregadas do arquivo YAML. |
|     297                           |         """                       |
|     298                           |         try:                      |
|     299                           |                                   |
|     300                           |            with serial.Serial(por |
|     301                           | ta, baud_rate, timeout=1) as ser: |
|     302                           |                                   |
| :::                               |      if isinstance(comando, str): |
|                                   |                                   |
|                                   |        comando = comando.encode() |
|                                   |                                   |
|                                   |                ser.write(comando) |
|                                   |                 log.a             |
|                                   | ppend(f"✅ Comando enviado (inter |
|                                   | no): {comando.decode().strip()}") |
|                                   |         ex                        |
|                                   | cept serial.SerialException as e: |
|                                   |             log.                  |
|                                   | append(f"❌ Erro ao enviar comand |
|                                   | o para a porta serial: {str(e)}") |
|                                   |         except Exception as e:    |
|                                   |             log.append            |
|                                   | (f"❌ Erro inesperado: {str(e)}") |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::
::::
:::::

::::: {.doc .doc-object .doc-function}
### [`exibir_analise_xor`{.highlight .language-python}]{.n}[`(`{.highlight .language-python}]{.p}[`raw_response`{.highlight .language-python}]{.n}[`)`{.highlight .language-python}]{.p} {#dashboard.github_dashboard.GitHubDashboard.exibir_analise_xor .doc .doc-heading}

:::: {.doc .doc-contents}
Exibe as informações do relay, com base em uma análise XOR.

[Returns:]{.doc-section-title}

+-----------------------+-----------------------+-----------------------+
| Name                  | Type                  | Description           |
+=======================+=======================+=======================+
| `Show`                | [`Xor`]{title="Xor"}  | :                     |
|                       |                       | :: doc-md-description |
|                       |                       | Configurações         |
|                       |                       | carregadas do arquivo |
|                       |                       | YAML.                 |
|                       |                       | :::                   |
+-----------------------+-----------------------+-----------------------+

Source code in `dashboard\github_dashboard.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|     374                           |                                   |
|     375                           |     def exibir_analise            |
|     376                           | _xor(self, raw_response) -> None: |
|     377                           |         """                       |
|     378                           |                                   |
|     379                           |        Exibe as informações do re |
|     380                           | lay, com base em uma análise XOR. |
|     381                           |                                   |
|     382                           |         Returns:                  |
|     383                           |             Show (Xor): Configur  |
|     384                           | ações carregadas do arquivo YAML. |
|     385                           |         """                       |
|     386                           |                                   |
|     387                           |  st.subheader("🧪 Análise XOR Bru |
|     388                           | te Force - Tabela Redimensional") |
|     389                           |         palavras_chave = ["OK     |
|     390                           | ", "FIREWALL", "ACCESS", "RESTART |
|     391                           | ", "DENIED", "GRANTED", "SECURE"] |
|     392                           |         tabela_xor = []           |
|     393                           |                                   |
|     394                           |         for key in range(1, 256): |
|     395                           |             xor_result            |
|     396                           | = [b ^ key for b in raw_response] |
|     397                           |             decode                |
|     398                           | d = ''.join(chr(b) if 32 <= b <=  |
|     399                           | 126 else '.' for b in xor_result) |
|     400                           |                                   |
|     401                           |             palavras_detect       |
|     402                           | adas = [p for p in palavras_chave |
|     403                           |  if p.upper() in decoded.upper()] |
|     404                           |                                   |
|     405                           |   printable_chars = sum(1 for c i |
|     406                           | n decoded if 32 <= ord(c) <= 126) |
|     407                           |             printable_ratio       |
|     408                           |  = printable_chars / len(decoded) |
|     409                           |                                   |
|     410                           |             if printable_rat      |
|     411                           | io > 0.8 and palavras_detectadas: |
| :::                               |                                   |
|                                   |               tabela_xor.append({ |
|                                   |                     "Key": key,   |
|                                   |                     "P            |
|                                   | rintable Ratio": printable_ratio, |
|                                   |                                   |
|                                   |                    "Qtd Palavras- |
|                                   | chave": len(palavras_detectadas), |
|                                   |                                   |
|                                   |         "Palavra-chave Detectada" |
|                                   | : ", ".join(palavras_detectadas), |
|                                   |                                   |
|                                   |     "Texto Decodificado": decoded |
|                                   |                 })                |
|                                   |                                   |
|                                   |         if tabela_xor:            |
|                                   |             df_xor =              |
|                                   | pd.DataFrame(tabela_xor).sort_val |
|                                   | ues(by=["Qtd Palavras-chave", "Pr |
|                                   | intable Ratio"], ascending=False) |
|                                   |                                   |
|                                   |                                   |
|                                   |     melhor_linha = df_xor.iloc[0] |
|                                   |                                   |
|                                   |    st.markdown("### 🔍 Insights") |
|                                   |                                   |
|                                   |         st.write(f"**Chave Encont |
|                                   | rada:** `{melhor_linha['Key']}`") |
|                                   |             st.write(             |
|                                   | f"**Texto Decodificado:** `{melho |
|                                   | r_linha['Texto Decodificado']}`") |
|                                   |             st.write(f"**Palavras |
|                                   | -chave Detectadas:** `{melhor_lin |
|                                   | ha['Palavra-chave Detectada']}`") |
|                                   |             st.writ               |
|                                   | e(f"**Printable Ratio:** `{melhor |
|                                   | _linha['Printable Ratio']:.2f}`") |
|                                   |             st.write(             |
|                                   | f"**Qtd Palavras-chave:** `{melho |
|                                   | r_linha['Qtd Palavras-chave']}`") |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::
::::
:::::

::::: {.doc .doc-object .doc-function}
### [`exibir_data_science`{.highlight .language-python}]{.n}[`()`{.highlight .language-python}]{.p} {#dashboard.github_dashboard.GitHubDashboard.exibir_data_science .doc .doc-heading}

:::: {.doc .doc-contents}
Exibe a lista de métodos datascience no aplicative.

[Returns:]{.doc-section-title}

+-----------------------+-----------------------+-----------------------+
| Name                  | Type                  | Description           |
+=======================+=======================+=======================+
| `Show`                | `None`                | :                     |
|                       |                       | :: doc-md-description |
|                       |                       | Configurações         |
|                       |                       | carregadas do arquivo |
|                       |                       | YAML.                 |
|                       |                       | :::                   |
+-----------------------+-----------------------+-----------------------+

Source code in `dashboard\github_dashboard.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|     132                           |                                   |
|     133                           |     def e                         |
|     134                           | xibir_data_science(self) -> None: |
|     135                           |         """                       |
|     136                           |         Exibe a lista de m        |
|     137                           | étodos datascience no aplicative. |
|     138                           |                                   |
|     139                           |         Returns:                  |
|     140                           |             Show (None): Configur |
|     141                           | ações carregadas do arquivo YAML. |
|     142                           |         """                       |
|     143                           |                                   |
|     144                           |      aba1, aba2, aba3 = st.tabs([ |
|     145                           |             "📈 Data S            |
|     146                           | cience: Regression Table - Info", |
|     147                           |             "📈 Data S            |
|     148                           | cience: Regression Table - Plot", |
|     149                           |             "📊                   |
| :::                               |  Data Science: Séries Temporais"  |
|                                   |         ])                        |
|                                   |         with aba1:                |
|                                   |                                   |
|                                   | self.exibir_data_science_resumo() |
|                                   |         with aba2:                |
|                                   |                                   |
|                                   |   self.exibir_data_science_plot() |
|                                   |         with aba3:                |
|                                   |                                   |
|                                   |    self.exibir_series_temporais() |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::
::::
:::::

::::: {.doc .doc-object .doc-function}
### [`exibir_data_science_plot`{.highlight .language-python}]{.n}[`()`{.highlight .language-python}]{.p} {#dashboard.github_dashboard.GitHubDashboard.exibir_data_science_plot .doc .doc-heading}

:::: {.doc .doc-contents}
Método DataScience.

[Returns:]{.doc-section-title}

+-----------------------+-----------------------+-----------------------+
| Name                  | Type                  | Description           |
+=======================+=======================+=======================+
| `Show`                | [                     | :                     |
|                       | `Plot`]{title="Plot"} | :: doc-md-description |
|                       |                       | Configurações         |
|                       |                       | carregadas do arquivo |
|                       |                       | YAML.                 |
|                       |                       | :::                   |
+-----------------------+-----------------------+-----------------------+

Source code in `dashboard\github_dashboard.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|     175                           |                                   |
|     176                           |     def exibir                    |
|     177                           | _data_science_plot(self) -> None: |
|     178                           |         """                       |
|     179                           |         Método DataScience.       |
|     180                           |                                   |
|     181                           |         Returns:                  |
|     182                           |             Show (Plot): Configur |
|     183                           | ações carregadas do arquivo YAML. |
|     184                           |         """                       |
|     185                           |         st.subheader("📈 Data S   |
|     186                           | cience: Regression Table - Plot") |
|     187                           |         try:                      |
|     188                           |             linguagem =           |
|     189                           | self.user_data.get("language", 0) |
|     190                           |             repos = self          |
|     191                           | .user_data.get("public_repos", 0) |
|     192                           |             df = pd.DataFrame({   |
|     193                           |                                   |
|     194                           |               "linguagens": [ling |
|     195                           | uagem + i for i in range(-5, 5)], |
| :::                               |                 "repositorios":   |
|                                   | [repos + i for i in range(-5, 5)] |
|                                   |             })                    |
|                                   |                                   |
|                                   |          fig, ax = plt.subplots() |
|                                   |                                   |
|                                   |      sns.regplot(x="linguagens",  |
|                                   | y="repositorios", data=df, ax=ax) |
|                                   |             ax.set_title("Regr    |
|                                   | essão Linear: Linguagens vs Repos |
|                                   | itórios (Baseada no seu GitHub)") |
|                                   |             st.pyplot(fig)        |
|                                   |         except Exception as e:    |
|                                   |             st.error(f"Erro ao e  |
|                                   | xibir gráfico de regressão: {e}") |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::
::::
:::::

::::: {.doc .doc-object .doc-function}
### [`exibir_data_science_resumo`{.highlight .language-python}]{.n}[`()`{.highlight .language-python}]{.p} {#dashboard.github_dashboard.GitHubDashboard.exibir_data_science_resumo .doc .doc-heading}

:::: {.doc .doc-contents}
Método DataScience.

[Returns:]{.doc-section-title}

+-----------------------+-----------------------+-----------------------+
| Name                  | Type                  | Description           |
+=======================+=======================+=======================+
| `Show`                | [`Res                 | :                     |
|                       | umo`]{title="Resumo"} | :: doc-md-description |
|                       |                       | Configurações         |
|                       |                       | carregadas do arquivo |
|                       |                       | YAML.                 |
|                       |                       | :::                   |
+-----------------------+-----------------------+-----------------------+

Source code in `dashboard\github_dashboard.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|     151                           |                                   |
|     152                           |     def exibir_d                  |
|     153                           | ata_science_resumo(self) -> None: |
|     154                           |         """                       |
|     155                           |         Método DataScience.       |
|     156                           |                                   |
|     157                           |         Returns:                  |
|     158                           |                                   |
|     159                           |           Show (Resumo): Configur |
|     160                           | ações carregadas do arquivo YAML. |
|     161                           |         """                       |
|     162                           |         st.subheader("📈 Data S   |
|     163                           | cience: Regression Table - Info") |
|     164                           |         try:                      |
|     165                           |             linguagem =           |
|     166                           | self.user_data.get("language", 0) |
|     167                           |             repos = self          |
|     168                           | .user_data.get("public_repos", 0) |
|     169                           |             df = pd.DataFrame({   |
|     170                           |                                   |
|     171                           |               "linguagens": [ling |
|     172                           | uagem + i for i in range(-5, 5)], |
|     173                           |                 "repositorios":   |
| :::                               | [repos + i for i in range(-5, 5)] |
|                                   |             })                    |
|                                   |             X = df["linguagens"]  |
|                                   |                                   |
|                                   |            y = df["repositorios"] |
|                                   |                                   |
|                                   |      X_const = sm.add_constant(X) |
|                                   |                                   |
|                                   | modelo = sm.OLS(y, X_const).fit() |
|                                   |             st                    |
|                                   | .write("**Resumo da Regressão Lin |
|                                   | ear com seus dados do GitHub:**") |
|                                   |                                   |
|                                   |         st.text(modelo.summary()) |
|                                   |         except Exception as e:    |
|                                   |             st.error(             |
|                                   | f"Erro ao exibir regressão: {e}") |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::
::::
:::::

::::: {.doc .doc-object .doc-function}
### [`exibir_lista_repositorios`{.highlight .language-python}]{.n}[`()`{.highlight .language-python}]{.p} {#dashboard.github_dashboard.GitHubDashboard.exibir_lista_repositorios .doc .doc-heading}

:::: {.doc .doc-contents}
Exibe a lista de repositórios detalhados no aplicative.

[Returns:]{.doc-section-title}

+-----------------------+-----------------------+-----------------------+
| Name                  | Type                  | Description           |
+=======================+=======================+=======================+
| `Show`                | `None`                | :                     |
|                       |                       | :: doc-md-description |
|                       |                       | Configurações         |
|                       |                       | carregadas do arquivo |
|                       |                       | YAML.                 |
|                       |                       | :::                   |
+-----------------------+-----------------------+-----------------------+

Source code in `dashboard\github_dashboard.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|     105                           |                                   |
|     106                           |     def exibir_                   |
|     107                           | lista_repositorios(self) -> None: |
|     108                           |         """                       |
|     109                           |         Exibe a lista de repos    |
|     110                           | itórios detalhados no aplicative. |
|     111                           |                                   |
|     112                           |         Returns:                  |
|     113                           |             Show (None): Configur |
|     114                           | ações carregadas do arquivo YAML. |
|     115                           |         """                       |
|     116                           |         st.subheader("📃          |
|     117                           | Lista Detalhada de Repositórios") |
|     118                           |         repos_url                 |
|     119                           | = self.user_data.get("repos_url") |
|     120                           |         if repos_url:             |
|     121                           |             try:                  |
|     122                           |                 repos             |
|     123                           |  = requests.get(repos_url).json() |
|     124                           |                                   |
|     125                           |        df_repos = pd.DataFrame([{ |
|     126                           |                                   |
|     127                           |             "Nome": repo["name"], |
|     128                           |                     "Descriç      |
|     129                           | ão": repo.get("description", ""), |
|     130                           |                     "Est          |
| :::                               | relas": repo["stargazers_count"], |
|                                   |                                   |
|                                   |     "Forks": repo["forks_count"], |
|                                   |                                   |
|                                   |          "URL": repo["html_url"], |
|                                   |                     "Linguag      |
|                                   | em": repo.get("language", "N/A"), |
|                                   |                     "A            |
|                                   | tualizado em": repo["updated_at"] |
|                                   |                                   |
|                                   |             } for repo in repos]) |
|                                   |                                   |
|                                   |            st.dataframe(df_repos) |
|                                   |                                   |
|                                   |            except Exception as e: |
|                                   |                 st.error(f"Err    |
|                                   | o ao carregar repositórios: {e}") |
|                                   |         else:                     |
|                                   |             st.warning("URL       |
|                                   | de repositórios não encontrada.") |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::
::::
:::::

::::: {.doc .doc-object .doc-function}
### [`exibir_perfil`{.highlight .language-python}]{.n}[`()`{.highlight .language-python}]{.p} {#dashboard.github_dashboard.GitHubDashboard.exibir_perfil .doc .doc-heading}

:::: {.doc .doc-contents}
Exibe o perfil do usuário do github.

[Returns:]{.doc-section-title}

+-----------------------+-----------------------+-----------------------+
| Name                  | Type                  | Description           |
+=======================+=======================+=======================+
| `Exibir`              | `None`                | :                     |
|                       |                       | :: doc-md-description |
|                       |                       | Configurações         |
|                       |                       | carregadas do arquivo |
|                       |                       | YAML.                 |
|                       |                       | :::                   |
+-----------------------+-----------------------+-----------------------+

Source code in `dashboard\github_dashboard.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|     50                            |                                   |
|     51                            |                                   |
|     52                            |  def exibir_perfil(self) -> None: |
|     53                            |         """                       |
|     54                            |         Exi                       |
|     55                            | be o perfil do usuário do github. |
|     56                            |                                   |
|     57                            |         Returns:                  |
|     58                            |                                   |
|     59                            |           Exibir (None): Configur |
|     60                            | ações carregadas do arquivo YAML. |
|     61                            |         """                       |
|     62                            |                                   |
|     63                            |   st.title("👤 GitHub Dashboard") |
|     64                            |                                   |
|     65                            |   col1, col2 = st.columns([1, 3]) |
|     66                            |         with col1:                |
|     67                            |             st.image(self.user_d  |
|     68                            | ata.get("avatar_url"), width=120) |
|     69                            |         with col2:                |
| :::                               |             st.su                 |
|                                   | bheader(self.user_data.get("name" |
|                                   | ) or self.user_data.get("login")) |
|                                   |             st.caption(f"[🔗      |
|                                   | {self.user_data.get('login')}]({s |
|                                   | elf.user_data.get('html_url')})") |
|                                   |             i                     |
|                                   | f self.user_data.get("location"): |
|                                   |                 st.text(f"        |
|                                   | 📍 {self.user_data['location']}") |
|                                   |                                   |
|                                   |   if self.user_data.get("email"): |
|                                   |                 st.text           |
|                                   | (f"📧 {self.user_data['email']}") |
|                                   |                                   |
|                                   |     if self.user_data.get("bio"): |
|                                   |                 st.markdow        |
|                                   | n(f"> _{self.user_data['bio']}_") |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::
::::
:::::

::::: {.doc .doc-object .doc-function}
### [`exibir_relay_firewall`{.highlight .language-python}]{.n}[`()`{.highlight .language-python}]{.p} {#dashboard.github_dashboard.GitHubDashboard.exibir_relay_firewall .doc .doc-heading}

:::: {.doc .doc-contents}
Exibe as informações do relay.

[Returns:]{.doc-section-title}

+-----------------------+-----------------------+-----------------------+
| Name                  | Type                  | Description           |
+=======================+=======================+=======================+
| `Show`                | [`R                   | :                     |
|                       | elay`]{title="Relay"} | :: doc-md-description |
|                       |                       | Configurações         |
|                       |                       | carregadas do arquivo |
|                       |                       | YAML.                 |
|                       |                       | :::                   |
+-----------------------+-----------------------+-----------------------+

Source code in `dashboard\github_dashboard.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|     233                           |                                   |
|     234                           |     def exi                       |
|     235                           | bir_relay_firewall(self) -> None: |
|     236                           |         """                       |
|     237                           |                                   |
|     238                           |    Exibe as informações do relay. |
|     239                           |                                   |
|     240                           |         Returns:                  |
|     241                           |                                   |
|     242                           |            Show (Relay): Configur |
|     243                           | ações carregadas do arquivo YAML. |
|     244                           |         """                       |
|     245                           |         log = []                  |
|     246                           |                                   |
|     247                           |         st.subheader("🚀 C        |
|     248                           | ibersegurança: Relay e Firewall") |
|     249                           |         status = st.empty()       |
|     250                           |         reiniciar                 |
|     251                           |  = st.button("💡 Reiniciar Relé") |
|     252                           |                                   |
|     253                           |         porta_serial = self.      |
|     254                           | detectar_porta_serial() or "COM4" |
|     255                           |         baud_rate = 9600          |
|     256                           |                                   |
|     257                           |         try:                      |
|     258                           |             if reiniciar:         |
|     259                           |                                   |
|     260                           |   st.write("Reiniciando relé...") |
|     261                           |                 log               |
|     262                           | = ["✅ Comando enviado: RESTART"] |
|     263                           |                                   |
|     264                           |    self.enviar_comando(porta_seri |
|     265                           | al, baud_rate, b"RESTART\n", log) |
|     266                           |                 status.success("  |
|     267                           | Relé Reiniciado com sucesso! ✅") |
|     268                           |                                   |
|     269                           |             st.inf                |
|     270                           | o(f"🔌 Iniciando comunicação seri |
|     271                           | al na porta `{porta_serial}`...") |
| :::                               |                                   |
|                                   |     with serial.Serial(porta_seri |
|                                   | al, baud_rate, timeout=2) as ser: |
|                                   |                 time.sleep(2)     |
|                                   |                                   |
|                                   |          ser.write(b"FIREWALL\n") |
|                                   |                 log =             |
|                                   |  ["✅ Comando enviado: FIREWALL"] |
|                                   |                                   |
|                                   |               start = time.time() |
|                                   |                                   |
|                                   |     raw_response = ser.readline() |
|                                   |                                   |
|                                   |    latencia = time.time() - start |
|                                   |                                   |
|                                   |             if log:               |
|                                   |                 self.exibir_resul |
|                                   | tado(raw_response, latencia, log) |
|                                   |                                   |
|                                   |         exc                       |
|                                   | ept serial.SerialException as se: |
|                                   |             st.error              |
|                                   | (f"Erro de conexão serial: {se}") |
|                                   |         except Exception as e:    |
|                                   |                                   |
|                                   | st.error(f"Erro inesperado: {e}") |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::
::::
:::::

::::: {.doc .doc-object .doc-function}
### [`exibir_repositorios`{.highlight .language-python}]{.n}[`()`{.highlight .language-python}]{.p} {#dashboard.github_dashboard.GitHubDashboard.exibir_repositorios .doc .doc-heading}

:::: {.doc .doc-contents}
Exibe a lista de repositórios no aplicative.

[Returns:]{.doc-section-title}

+-----------------------+-----------------------+-----------------------+
| Name                  | Type                  | Description           |
+=======================+=======================+=======================+
| `Show`                | `None`                | :                     |
|                       |                       | :: doc-md-description |
|                       |                       | Configurações         |
|                       |                       | carregadas do arquivo |
|                       |                       | YAML.                 |
|                       |                       | :::                   |
+-----------------------+-----------------------+-----------------------+

Source code in `dashboard\github_dashboard.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|     71                            |                                   |
|     72                            |     def e                         |
|     73                            | xibir_repositorios(self) -> None: |
|     74                            |         """                       |
|     75                            |         Exibe a lis               |
|     76                            | ta de repositórios no aplicative. |
|     77                            |                                   |
|     78                            |         Returns:                  |
|     79                            |             Show (None): Configur |
|     80                            | ações carregadas do arquivo YAML. |
|     81                            |         """                       |
|     82                            |         aba1, aba2 = st.tabs(     |
| :::                               | ["📦 Repositórios Públicos", "🗃️ L |
|                                   | ista Detalhada de Repositórios"]) |
|                                   |         with aba1:                |
|                                   |             se                    |
|                                   | lf.exibir_repositorios_publicos() |
|                                   |         with aba2:                |
|                                   |                                   |
|                                   |  self.exibir_lista_repositorios() |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::
::::
:::::

::::: {.doc .doc-object .doc-function}
### [`exibir_repositorios_publicos`{.highlight .language-python}]{.n}[`()`{.highlight .language-python}]{.p} {#dashboard.github_dashboard.GitHubDashboard.exibir_repositorios_publicos .doc .doc-heading}

:::: {.doc .doc-contents}
Exibe a lista de repositórios publicos no aplicative.

[Returns:]{.doc-section-title}

+-----------------------+-----------------------+-----------------------+
| Name                  | Type                  | Description           |
+=======================+=======================+=======================+
| `Show`                | `None`                | :                     |
|                       |                       | :: doc-md-description |
|                       |                       | Configurações         |
|                       |                       | carregadas do arquivo |
|                       |                       | YAML.                 |
|                       |                       | :::                   |
+-----------------------+-----------------------+-----------------------+

Source code in `dashboard\github_dashboard.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|      84                           |                                   |
|      85                           |     def exibir_rep                |
|      86                           | ositorios_publicos(self) -> None: |
|      87                           |         """                       |
|      88                           |         Exibe a lista de rep      |
|      89                           | ositórios publicos no aplicative. |
|      90                           |                                   |
|      91                           |         Returns:                  |
|      92                           |             Show (None): Configur |
|      93                           | ações carregadas do arquivo YAML. |
|      94                           |         """                       |
|      95                           |         st.subh                   |
|      96                           | eader("📦 Repositórios Públicos") |
|      97                           |         repos_url                 |
|      98                           | = self.user_data.get("repos_url") |
|      99                           |         if repos_url:             |
|     100                           |             r                     |
|     101                           | esponse = requests.get(repos_url) |
|     102                           |                                   |
|     103                           |   if response.status_code == 200: |
| :::                               |                                   |
|                                   |           repos = response.json() |
|                                   |                                   |
|                                   |       if isinstance(repos, list): |
|                                   |                                   |
|                                   |          for repo in repos[:100]: |
|                                   |                                   |
|                                   |             st.markdown(f"📔️ [{re |
|                                   | po['name']}]({repo['html_url']})  |
|                                   | — ⭐ {repo['stargazers_count']}") |
|                                   |                 else:             |
|                                   |                     st.warning    |
|                                   | ("\u26a0\ufe0f Dados de repositór |
|                                   | ios inválidos recebidos da API.") |
|                                   |             else:                 |
|                                   |                 st                |
|                                   | .error(f"❌ Erro ao acessar repos |
|                                   | itórios: {response.status_code}") |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::
::::
:::::

::::: {.doc .doc-object .doc-function}
### [`exibir_resultado`{.highlight .language-python}]{.n}[`(`{.highlight .language-python}]{.p}[`raw_response`{.highlight .language-python}]{.n}[`,`{.highlight .language-python}]{.p}` `{.highlight .language-python}[`latencia`{.highlight .language-python}]{.n}[`,`{.highlight .language-python}]{.p}` `{.highlight .language-python}[`log`{.highlight .language-python}]{.n}[`)`{.highlight .language-python}]{.p} {#dashboard.github_dashboard.GitHubDashboard.exibir_resultado .doc .doc-heading}

:::: {.doc .doc-contents}
Exibe o resultado das informações do relay.

[Returns:]{.doc-section-title}

+-----------------------+-----------------------+-----------------------+
| Name                  | Type                  | Description           |
+=======================+=======================+=======================+
| `Show`                | [`R                   | :                     |
|                       | elay`]{title="Relay"} | :: doc-md-description |
|                       |                       | Configurações         |
|                       |                       | carregadas do arquivo |
|                       |                       | YAML.                 |
|                       |                       | :::                   |
+-----------------------+-----------------------+-----------------------+

Source code in `dashboard\github_dashboard.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|     304                           |                                   |
|     305                           |                                   |
|     306                           |   def exibir_resultado(self, raw_ |
|     307                           | response, latencia, log) -> None: |
|     308                           |         """                       |
|     309                           |         Exibe o re                |
|     310                           | sultado das informações do relay. |
|     311                           |                                   |
|     312                           |         Returns:                  |
|     313                           |                                   |
|     314                           |            Show (Relay): Configur |
|     315                           | ações carregadas do arquivo YAML. |
|     316                           |         """                       |
|     317                           |                                   |
|     318                           |        response_str = self.decodi |
|     319                           | ficar_resposta(raw_response, log) |
|     320                           |                                   |
|     321                           |  abas = st.tabs(["📱 Resposta", " |
|     322                           | 📦 Bytes Recebidos", "🧾 Log de D |
|     323                           | ecodificação", "🧪 Análise XOR"]) |
|     324                           |                                   |
|     325                           |         with abas[0]:             |
|     326                           |             st.subhea             |
|     327                           | der("📱 Resposta do Dispositivo") |
|     328                           |             if response_str:      |
|     329                           |                                   |
|     330                           |          st.success(f"📱 Resposta |
|     331                           |  do dispositivo: {response_str}") |
|     332                           |             else:                 |
|     333                           |                 st.warning("      |
|     334                           | ⚠️ Dados não textuais recebidos.") |
|     335                           |                 st.code(raw       |
|     336                           | _response.hex(), language="text") |
|     337                           |                                   |
|     338                           |                                   |
|     339                           |           st.text(f"⏱️ Tempo de re |
|     340                           | sposta: {latencia:.2f} segundos") |
|     341                           |                                   |
|     342                           |             if response_str       |
|     343                           | and "OK" in response_str.upper(): |
|     344                           |                 st.success("🔍 Fi |
|     345                           | rewall validado e relay seguro.") |
|     346                           |             elif response_str:    |
| :::                               |                 st.warning(f"     |
|                                   | ❗ Resposta inesperada: '{respons |
|                                   | e_str}' — verifique o firmware.") |
|                                   |             else:                 |
|                                   |                                   |
|                                   |           st.error("❌ Nenhuma re |
|                                   | sposta válida foi interpretada.") |
|                                   |                                   |
|                                   |         with abas[1]:             |
|                                   |             st                    |
|                                   | .code(" ".join(f"{b:02x}" for b i |
|                                   | n raw_response), language="text") |
|                                   |                                   |
|                                   |       byte_table = pd.DataFrame({ |
|                                   |                 "Byte (Hex)": [f  |
|                                   | "{b:02x}" for b in raw_response], |
|                                   |                 "Byte (Dec)"      |
|                                   | : [str(b) for b in raw_response], |
|                                   |                                   |
|                                   | "ASCII": [chr(b) if 32 <= b <= 12 |
|                                   | 6 else "." for b in raw_response] |
|                                   |             })                    |
|                                   |             with s                |
|                                   | t.expander("📦 Bytes Recebidos"): |
|                                   |                                   |
|                                   |          st.dataframe(byte_table) |
|                                   |                                   |
|                                   |         with abas[2]:             |
|                                   |             st.sub                |
|                                   | header("🧾 Log de Decodificação") |
|                                   |             st.code               |
|                                   | ("\n".join(log), language="text") |
|                                   |                                   |
|                                   |         with abas[3]:             |
|                                   |             self                  |
|                                   | .exibir_analise_xor(raw_response) |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::
::::
:::::

::::: {.doc .doc-object .doc-function}
### [`exibir_series_temporais`{.highlight .language-python}]{.n}[`()`{.highlight .language-python}]{.p} {#dashboard.github_dashboard.GitHubDashboard.exibir_series_temporais .doc .doc-heading}

:::: {.doc .doc-contents}
Método DataScience.

[Returns:]{.doc-section-title}

+-----------------------+-----------------------+-----------------------+
| Name                  | Type                  | Description           |
+=======================+=======================+=======================+
| `Show`                | [`Temporais           | :                     |
|                       | `]{title="Temporais"} | :: doc-md-description |
|                       |                       | Configurações         |
|                       |                       | carregadas do arquivo |
|                       |                       | YAML.                 |
|                       |                       | :::                   |
+-----------------------+-----------------------+-----------------------+

Source code in `dashboard\github_dashboard.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|     197                           |                                   |
|     198                           |     def exibi                     |
|     199                           | r_series_temporais(self) -> None: |
|     200                           |         """                       |
|     201                           |         Método DataScience.       |
|     202                           |                                   |
|     203                           |         Returns:                  |
|     204                           |                                   |
|     205                           |        Show (Temporais): Configur |
|     206                           | ações carregadas do arquivo YAML. |
|     207                           |         """                       |
|     208                           |         st.su                     |
|     209                           | bheader("📊 Análise de Séries Tem |
|     210                           | porais com seus dados do GitHub") |
|     211                           |         try:                      |
|     212                           |             # Simula evolução     |
|     213                           | de repositórios com base no tempo |
|     214                           |             linguagem =           |
|     215                           | self.user_data.get("language", 0) |
|     216                           |             repos = self          |
|     217                           | .user_data.get("public_repos", 0) |
|     218                           |                                   |
|     219                           |        datas = pd.date_range(end= |
|     220                           | pd.Timestamp.today(), periods=10) |
|     221                           |                                   |
|     222                           |             df = pd.DataFrame({   |
|     223                           |                 "data": datas,    |
|     224                           |                 "linguagens": [l  |
|     225                           | inguagem + i for i in range(10)], |
|     226                           |                                   |
|     227                           |       "repositorios": [repos + i  |
|     228                           | + (i % 3 - 1) for i in range(10)] |
|     229                           |             }).set_index("data")  |
|     230                           |                                   |
| :::                               |                                   |
|                                   |        # Gráfico de linha simples |
|                                   |             st                    |
|                                   | .line_chart(df[["repositorios"]]) |
|                                   |                                   |
|                                   |             # Média móvel         |
|                                   |                                   |
|                                   |    df["media_movel"] = df["reposi |
|                                   | torios"].rolling(window=3).mean() |
|                                   |                                   |
|                                   |          fig, ax = plt.subplots() |
|                                   |                                   |
|                                   |   df["repositorios"].plot(ax=ax,  |
|                                   | label="Repositórios", marker="o") |
|                                   |             df["media             |
|                                   | _movel"].plot(ax=ax, label="Média |
|                                   |  Móvel (3 dias)", linestyle="--") |
|                                   |             ax                    |
|                                   | .set_title("Repositórios GitHub - |
|                                   |  Série Temporal com Média Móvel") |
|                                   |             ax.legend()           |
|                                   |             st.pyplot(fig)        |
|                                   |                                   |
|                                   |         except Exception as e:    |
|                                   |             st.error(f"Erro       |
|                                   | ao exibir séries temporais: {e}") |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::
::::
:::::

::::: {.doc .doc-object .doc-function}
### [`show_dashboard`{.highlight .language-python}]{.n}[`()`{.highlight .language-python}]{.p} {#dashboard.github_dashboard.GitHubDashboard.show_dashboard .doc .doc-heading}

:::: {.doc .doc-contents}
Exibe a lista de funcionalidades no aplicative.

[Returns:]{.doc-section-title}

+-----------------------+-----------------------+-----------------------+
| Name                  | Type                  | Description           |
+=======================+=======================+=======================+
| `Show`                | `None`                | :                     |
|                       |                       | :: doc-md-description |
|                       |                       | Configurações         |
|                       |                       | carregadas do arquivo |
|                       |                       | YAML.                 |
|                       |                       | :::                   |
+-----------------------+-----------------------+-----------------------+

Source code in `dashboard\github_dashboard.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|     16                            |                                   |
|     17                            |                                   |
|     18                            | def show_dashboard(self) -> None: |
|     19                            |         """                       |
|     20                            |         Exibe a lista             |
|     21                            | de funcionalidades no aplicative. |
|     22                            |                                   |
|     23                            |         Returns:                  |
|     24                            |             Show (None): Configur |
|     25                            | ações carregadas do arquivo YAML. |
|     26                            |         """                       |
|     27                            |         tabs = st.tabs([          |
|     28                            |             "👤 Perfil",          |
|     29                            |                                   |
|     30                            |       "📦 Repositórios Públicos", |
|     31                            |             "🗃️ Lista Detalhada", |
|     32                            |                                   |
|     33                            |            "📊 Regressão - Info", |
|     34                            |                                   |
|     35                            |         "📉 Regressão - Gráfico", |
|     36                            |             "🛡️ Relay e Firewall" |
|     37                            |         ])                        |
|     38                            |                                   |
|     39                            |         with tabs[0]:             |
|     40                            |             self.exibir_perfil()  |
|     41                            |                                   |
|     42                            |         with tabs[1]:             |
|     43                            |             se                    |
|     44                            | lf.exibir_repositorios_publicos() |
|     45                            |                                   |
|     46                            |         with tabs[2]:             |
|     47                            |                                   |
|     48                            |  self.exibir_lista_repositorios() |
| :::                               |                                   |
|                                   |         with tabs[3]:             |
|                                   |                                   |
|                                   |        self.exibir_data_science() |
|                                   |                                   |
|                                   |         with tabs[4]:             |
|                                   |                                   |
|                                   |   self.exibir_data_science_plot() |
|                                   |                                   |
|                                   |         with tabs[5]:             |
|                                   |                                   |
|                                   |      self.exibir_relay_firewall() |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::
::::
:::::
::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::: {.doc .doc-object .doc-module}
[]{#blackops.ui.streamlit_interface}

:::::::::::::::: {.doc .doc-contents .first}
::::::::::::::: {.doc .doc-children}
::::: {.doc .doc-object .doc-function}
## [`executar_funcao`{.highlight .language-python}]{.n}[`(`{.highlight .language-python}]{.p}[`funcao`{.highlight .language-python}]{.n}[`)`{.highlight .language-python}]{.p} {#blackops.ui.streamlit_interface.executar_funcao .doc .doc-heading}

:::: {.doc .doc-contents}
Executa a função associada a um botão da interface Streamlit.

[Returns:]{.doc-section-title}

+-----------------------+-----------------------+-----------------------+
| Name                  | Type                  | Description           |
+=======================+=======================+=======================+
| `Funcao`              | [`Optional`]{title="t | :                     |
|                       | yping.Optional"}`[`[` | :: doc-md-description |
|                       | str`]{title="str"}`]` | Nome da função a ser  |
|                       |                       | executada.            |
|                       |                       | :::                   |
+-----------------------+-----------------------+-----------------------+

Source code in `blackops\ui\streamlit_interface.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|     120                           |                                   |
|     121                           |     def executar_funca            |
|     122                           | o(funcao: Optional[str]) -> None: |
|     123                           |         """                       |
|     124                           |                                   |
|     125                           |      Executa a função associada a |
|     126                           |  um botão da interface Streamlit. |
|     127                           |                                   |
|     128                           |         Returns:                  |
|     129                           |                                   |
|     130                           |            Funcao (Optional[str]) |
|     131                           | : Nome da função a ser executada. |
|     132                           |         """                       |
|     133                           |                                   |
|     134                           |    if funcao == 'activate_relay': |
|     135                           |             activate_relay()      |
|     136                           |             st.succ               |
|     137                           | ess("Relay ativado com sucesso!") |
|     138                           |                                   |
|     139                           |       elif funcao == 'scan_port': |
|     140                           |             portas = scan_ports() |
|     141                           |             st.                   |
| :::                               | code(f"Portas abertas: {portas}") |
|                                   |                                   |
|                                   | elif funcao == 'verify_firewall': |
|                                   |                                   |
|                                   |   regras = check_firewall_rules() |
|                                   |                                   |
|                                   |        st.code("\n".join(regras)) |
|                                   |                                   |
|                                   |   elif funcao == 'voice_command': |
|                                   |             res                   |
|                                   | ultado = activate_voice_control() |
|                                   |             st.success(resultado) |
|                                   |             st.info(resultado)    |
|                                   |                                   |
|                                   |   elif funcao == 'stream_camera': |
|                                   |             stream_camera()       |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::
::::
:::::

::::: {.doc .doc-object .doc-function}
## [`load_config`{.highlight .language-python}]{.n}[`()`{.highlight .language-python}]{.p} {#blackops.ui.streamlit_interface.load_config .doc .doc-heading}

:::: {.doc .doc-contents}
Carrega o arquivo de configuração YAML.

[Returns:]{.doc-section-title}

+-----------------------+-----------------------+-----------------------+
| Name                  | Type                  | Description           |
+=======================+=======================+=======================+
| `Load`                | [`                    | :                     |
|                       | Dict`]{title="typing. | :: doc-md-description |
|                       | Dict"}`[`[`str`]{titl | Configurações         |
|                       | e="str"}`, `[`Any`]{t | carregadas do arquivo |
|                       | itle="typing.Any"}`]` | YAML.                 |
|                       |                       | :::                   |
+-----------------------+-----------------------+-----------------------+

Source code in `blackops\ui\streamlit_interface.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|     17                            |                                   |
|     18                            |     def                           |
|     19                            |  load_config() -> Dict[str, Any]: |
|     20                            |         """                       |
|     21                            |         Carreg                    |
|     22                            | a o arquivo de configuração YAML. |
|     23                            |                                   |
|     24                            |         Returns:                  |
|     25                            |             Load: Configur        |
|     26                            | ações carregadas do arquivo YAML. |
| :::                               |         """                       |
|                                   |         config_path = os.pat      |
|                                   | h.join(os.path.dirname(__file__), |
|                                   |  '..', 'config', 'settings.yaml') |
|                                   |         wit                       |
|                                   | h open(config_path, 'r') as file: |
|                                   |                                   |
|                                   |       return yaml.safe_load(file) |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::
::::
:::::

::::: {.doc .doc-object .doc-function}
## [`show_comandos_disponiveis`{.highlight .language-python}]{.n}[`()`{.highlight .language-python}]{.p} {#blackops.ui.streamlit_interface.show_comandos_disponiveis .doc .doc-heading}

:::: {.doc .doc-contents}
Exibe a lista de comandos de voz disponíveis na interface Streamlit.

[Returns:]{.doc-section-title}

+-----------------------+-----------------------+-----------------------+
| Name                  | Type                  | Description           |
+=======================+=======================+=======================+
| `Show`                | `None`                | :                     |
|                       |                       | :: doc-md-description |
|                       |                       | Configurações         |
|                       |                       | carregadas do arquivo |
|                       |                       | YAML.                 |
|                       |                       | :::                   |
+-----------------------+-----------------------+-----------------------+

Source code in `blackops\ui\streamlit_interface.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|     29                            |                                   |
|     30                            |     def sho                       |
|     31                            | w_comandos_disponiveis() -> None: |
|     32                            |         """                       |
|     33                            |         Ex                        |
|     34                            | ibe a lista de comandos de voz di |
|     35                            | sponíveis na interface Streamlit. |
|     36                            |                                   |
|     37                            |         Returns:                  |
|     38                            |             Show (None): Configur |
|     39                            | ações carregadas do arquivo YAML. |
|     40                            |         """                       |
|     41                            |         st.markdown("---")        |
|     42                            |         st.markdown("##           |
|     43                            | # 🎙️ Comandos de Voz Disponíveis") |
|     44                            |         comandos = [              |
|     45                            |             "Q                    |
|     46                            | ual o último commit do projeto?", |
| :::                               |             "Resum                |
|                                   | a o repositório OpenAI Whisper.", |
|                                   |                                   |
|                                   |  "Quantas issues estão abertas?", |
|                                   |                                   |
|                                   |    "Quais são as pull requests?", |
|                                   |             "Em qual linguagem e  |
|                                   | sse repositório está programado?" |
|                                   |         ]                         |
|                                   |         for comando in comandos:  |
|                                   |                                   |
|                                   |     st.markdown(f"- `{comando}`") |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::
::::
:::::

::::: {.doc .doc-object .doc-function}
## [`show_project_info`{.highlight .language-python}]{.n}[`()`{.highlight .language-python}]{.p} {#blackops.ui.streamlit_interface.show_project_info .doc .doc-heading}

:::: {.doc .doc-contents}
Exibe informações do repositório GitHub, comandos e ações interativas na
interface Streamlit.

[Returns:]{.doc-section-title}

+-----------------------+-----------------------+-----------------------+
| Name                  | Type                  | Description           |
+=======================+=======================+=======================+
| `Project`             | `None`                | :                     |
|                       |                       | :: doc-md-description |
|                       |                       | Configurações         |
|                       |                       | carregadas do arquivo |
|                       |                       | YAML.                 |
|                       |                       | :::                   |
+-----------------------+-----------------------+-----------------------+

Source code in `blackops\ui\streamlit_interface.py`

::: highlight
+-----------------------------------+-----------------------------------+
| ::: linenodiv                     | <div>                             |
|      49                           |                                   |
|      50                           |                                   |
|      51                           |  def show_project_info() -> None: |
|      52                           |         """                       |
|      53                           |                                   |
|      54                           |       Exibe informações do reposi |
|      55                           | tório GitHub, comandos e ações in |
|      56                           | terativas na interface Streamlit. |
|      57                           |                                   |
|      58                           |         Returns:                  |
|      59                           |                                   |
|      60                           |          Project (None): Configur |
|      61                           | ações carregadas do arquivo YAML. |
|      62                           |         """                       |
|      63                           |                                   |
|      64                           |         col_sta                   |
|      65                           | tus, col_comandos = st.columns(2) |
|      66                           |                                   |
|      67                           |         config = load_config()    |
|      68                           |         st_autorefresh(interval=  |
|      69                           | 60000, key="github_auto_refresh") |
|      70                           |                                   |
|      71                           |         with col_status:          |
|      72                           |             st.markdown("---")    |
|      73                           |             st.header("           |
|      74                           | 📡 Status do Repositório GitHub") |
|      75                           |                                   |
|      76                           |                                   |
|      77                           |      token = os.getenv("8928341d3 |
|      78                           | b422e184b621364a45885f6a2baa804") |
|      79                           |                                   |
|      80                           |      repo_name = "openai/whisper" |
|      81                           |                                   |
|      82                           |             repo_info             |
|      83                           | = get_repo_info(repo_name, token) |
|      84                           |                                   |
|      85                           |                                   |
|      86                           |          if "error" in repo_info: |
|      87                           |                                   |
|      88                           |  st.error(f"Erro ao buscar dados  |
|      89                           | do GitHub: {repo_info['error']}") |
|      90                           |             else:                 |
|      91                           |                                   |
|      92                           |          st.markdown(f"**🔗 Repos |
|      93                           | itório:** `{repo_info['name']}`") |
|      94                           |                                   |
|      95                           |      st.markdown(f"**📝 Descrição |
|      96                           | :** {repo_info['description']}`") |
|      97                           |                 st.               |
|      98                           | markdown(f"**📦 Linguagem Princip |
|      99                           | al:** `{repo_info['language']}`") |
|     100                           |                                   |
|     101                           |            st.markdown(f"**⭐ Est |
|     102                           | relas:** `{repo_info['stars']}`") |
|     103                           |                 s                 |
|     104                           | t.markdown(f"**🐞 Issues Abertas: |
|     105                           | ** `{repo_info['open_issues']}`") |
|     106                           |                                   |
|     107                           | st.markdown(f"**🕒 Último Commit: |
|     108                           | ** `{repo_info['last_commit']}`") |
|     109                           |                                   |
|     110                           |         with col_comandos:        |
|     111                           |                                   |
|     112                           |       show_comandos_disponiveis() |
|     113                           |                                   |
|     114                           |         st.markdown("---")        |
|     115                           |         st                        |
|     116                           | .header("⚙️ Comandos de Controle") |
|     117                           |                                   |
| :::                               |         col1, col2,               |
|                                   |  col3, col4, col5 = st.columns(5) |
|                                   |                                   |
|                                   |      funcao: Optional[str] = None |
|                                   |                                   |
|                                   |         with col1:                |
|                                   |                                   |
|                                   |  if st.button("Ativar Relay 🔌"): |
|                                   |                                   |
|                                   |         funcao = 'activate_relay' |
|                                   |         with col2:                |
|                                   |             i                     |
|                                   | f st.button("Scan de Portas 🌐"): |
|                                   |                                   |
|                                   |              funcao = 'scan_port' |
|                                   |         with col3:                |
|                                   |             if st                 |
|                                   | .button("Verificar Firewall 🔥"): |
|                                   |                                   |
|                                   |        funcao = 'verify_firewall' |
|                                   |         with col4:                |
|                                   |                                   |
|                                   | if st.button("Comando de Voz 🎙️"): |
|                                   |                                   |
|                                   |          funcao = 'voice_command' |
|                                   |         with col5:                |
|                                   |             if st.but             |
|                                   | ton("📡 Iniciar Live da Câmera"): |
|                                   |                                   |
|                                   |          funcao = 'stream_camera' |
|                                   |                                   |
|                                   |         executar_funcao(funcao)   |
|                                   |                                   |
|                                   |         st.markdown("---")        |
|                                   |                                   |
|                                   | st.markdown("✅ Módulos Ativos:") |
|                                   |         st.markdown               |
|                                   | ("- 🔌 Controle de Relay (GPIO)") |
|                                   |         st.markdown("- 🌐 V       |
|                                   | erificador de Firewall e Portas") |
|                                   |         st.mark                   |
|                                   | down("- 🎙️ Reconhecimento de voz") |
|                                   |         st.markdown("             |
|                                   | - 📷 OCR e Transmissão de vídeo") |
|                                   |         st.markdo                 |
|                                   | wn("- 🧠 Módulos de IA e Física") |
|                                   |         st.mar                    |
|                                   | kdown("- 📊 Interface Streamlit") |
|                                   |                                   |
|                                   |         st.success("Siste         |
|                                   | ma pronto para operação tática.") |
|                                   |                                   |
|                                   | </div>                            |
+-----------------------------------+-----------------------------------+
:::
::::
:::::
:::::::::::::::
::::::::::::::::
:::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
