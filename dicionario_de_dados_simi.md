Com certeza! Ter um "dicionário de dados" claro é um passo fundamental para qualquer análise. Abaixo está a descrição detalhada de cada uma das 33 colunas do seu arquivo `simi_data_processed.csv`, agrupadas por categorias para facilitar a compreensão.

---

### Dicionário de Dados - SIMI

#### **1. Identificação e Contato da Organização**

_Estas colunas fornecem informações básicas para identificar, localizar e contatar a organização._

`cadastro_aprovado`

- **Significado:** Indica se o cadastro da organização foi revisado e aprovado pela equipe do SIMI para aparecer na plataforma.
- **Contexto/Exemplo:** Um valor "Sim" significa que a organização é um membro verificado do ecossistema.

`autorizacao_divulgacao`

- **Significado:** Confirma se a organização deu consentimento para que suas informações (fornecidas no formulário) fossem divulgadas publicamente na plataforma e em estudos.
- **Contexto/Exemplo:** Essencialmente uma coluna de consentimento (LGPD).

`nome_organizacao`

- **Significado:** O nome oficial ou fantasia da organização.
- **Contexto/Exemplo:** "Manuel VAIoT", "Prefeitura Municipal de Arcos".

`cidade_sede`

- **Significado:** A cidade onde a sede principal da organização está localizada.
- **Contexto/Exemplo:** Crucial para análises geográficas e mapeamento de polos de inovação. Ex: "Itajubá", "Belo Horizonte".

`uf_sede`

- **Significado:** A Unidade Federativa (Estado) da sede da organização.
- **Contexto/Exemplo:** No seu caso, o esperado é que a grande maioria seja "MG" (Minas Gerais).

`logo_url`

- **Significado:** O link (URL) para a imagem do logotipo da organização.
- **Contexto/Exemplo:** Útil para criar relatórios visuais, perfis ou dashboards.

`site_organizacao`

- **Significado:** O endereço do site oficial da organização.

`email_contato`

- **Significado:** O principal e-mail de contato fornecido pela organização.

`linkedin_url`

- **Significado:** O link para a página da organização no LinkedIn.

---

#### **2. Classificação e Perfil da Organização**

_Estas colunas categorizam a organização dentro do ecossistema SIMI, o que é vital para filtrar e segmentar a análise._

`categoria_organizacao`

- **Significado:** A principal categoria em que a organização se enquadra no ecossistema de inovação.
- **Contexto/Exemplo:** Esta é uma das colunas mais importantes para filtragem. Valores incluem: "Startup", "Governo Municipal", "ICT (Instituição de Ciência e Tecnologia)", "Investidor", "Incubadora/Aceleradora".

`tipo_organizacao`

- **Significado:** Uma sub-categoria ou um tipo mais específico de organização, geralmente preenchido por "Demais Organizações" que não se encaixam perfeitamente nas categorias principais.
- **Contexto/Exemplo:** Pode conter valores como "Associação", "Consultoria", "Escritório de Advocacia".

`possui_nit`

- **Significado:** Informa se a organização possui um NIT (Núcleo de Inovação Tecnológica).
- **Contexto/Exemplo:** Relevante principalmente para Universidades e ICTs, indicando uma estrutura formal para a gestão da propriedade intelectual.

`orgao_responsavel_cti`

- **Significado:** O departamento específico responsável pela pauta de Ciência, Tecnologia e Inovação (CTI).
- **Contexto/Exemplo:** Relevante para órgãos governamentais. Ex: "Secretaria de Desenvolvimento Econômico".

`incentivos_fiscais_municipio`

- **Significado:** Descreve os incentivos fiscais que um município oferece para empresas de base tecnológica.
- **Contexto/Exemplo:** Coluna preenchida quase exclusivamente pela categoria "Governo Municipal".

---

#### **3. Descrição do Negócio e Atuação**

_O coração dos dados, descrevendo o que a organização faz, para quem e como._

`descricao_organizacao`

- **Significado:** Um texto aberto onde a organização descreve suas atividades, missão e propósito.
- **Contexto/Exemplo:** É uma fonte riquíssima para buscas por palavras-chave que não são capturadas em outras colunas.

`segmento_atuacao`

- **Significado:** O principal mercado ou setor em que a organização atua.
- **Contexto/Exemplo:** Coluna fundamental para a análise da Nova Indústria Brasil. Ex: "Saúde", "Agro", "Fintech", "Educação".

`modelo_negocio`

- **Significado:** Como a organização gera receita ou entrega valor.
- **Contexto/Exemplo:** "SaaS", "Marketplace", "E-commerce", "Hardware".

`tecnologias_disruptivas`

- **Significado:** As principais tecnologias que a organização desenvolve ou utiliza.
- **Contexto/Exemplo:** Crucial para medir o nível de inovação e para a Missão 4 (Transformação Digital) da NIB. Ex: "Inteligência Artificial", "IOT", "Blockchain".

`segmentacao_clientes`

- **Significado:** O público-alvo principal da organização.
- **Contexto/Exemplo:** "B2B" (empresa para empresa), "B2C" (empresa para consumidor), "B2B2C" (empresa para empresa para consumidor).

`areas_expertise`

- **Significado:** Principais áreas do conhecimento ou competências técnicas da organização.
- **Contexto/Exemplo:** Muito usada por ICTs e consultorias para descrever suas especialidades.

---

#### **4. Maturidade e Tamanho**

_Estas colunas ajudam a entender o estágio de desenvolvimento e o porte da organização._

`fase_negocio`

- **Significado:** O estágio atual de desenvolvimento do negócio.
- **Contexto/Exemplo:** Essencial para entender a maturidade do ecossistema. Valores típicos: "Ideação", "Validação", "Operação", "Tração", "Scale-up".

`numero_funcionarios`

- **Significado:** O tamanho da equipe da organização, geralmente em faixas.
- **Contexto/Exemplo:** "1-5 funcionários", "11-50 funcionários".

---

#### **5. Investimento e Fomento**

_Colunas focadas em captação de recursos, investimentos realizados e programas de apoio._

`busca_investimento`

- **Significado:** Um indicador direto ("Sim" ou "Não") se a organização está ativamente procurando por investimento.
- **Contexto/Exemplo:** Um sinalizador chave para investidores e agências de fomento.

`fase_investimento_captada`

- **Significado:** O estágio de investimento mais recente que a organização **já recebeu**.
- **Contexto/Exemplo:** "Anjo", "Pré-Seed", "Seed", "Série A". Ajuda a entender a jornada de captação da empresa.

`fase_investimento_busca`

- **Significado:** O estágio de investimento que a organização está **procurando atualmente**.
- **Contexto/Exemplo:** "Seed", "Série A", etc. Mostra a demanda por capital no ecossistema.

`tese_investimento`

- **Significado:** Descreve os critérios e foco de um investidor.
- **Contexto/Exemplo:** Preenchido por organizações da categoria "Investidor". Ex: "Investimos em startups SaaS B2B em estágio Seed".

`num_startups_investidas`

- **Significado:** O número de startups no portfólio de um investidor ou aceleradora.

`investimento_medio_startup`

- **Significado:** O valor médio (check-size) que um investidor aporta por startup.

`exige_equity`

- **Significado:** Informa se um programa de aceleração/incubação exige participação acionária (equity) da startup.

---

#### **6. Detalhes Específicos e Programas**

_Colunas complementares, muitas vezes preenchidas por categorias específicas de organizações._

`programas_desenvolvimento`

- **Significado:** Descreve os programas (de aceleração, incubação, fomento) oferecidos pela organização.
- **Contexto/Exemplo:** Relevante para Incubadoras, Aceleradoras e Governo.

`beneficios_programa`

- **Significado:** Os benefícios específicos oferecidos pelos programas listados acima.
- **Contexto/Exemplo:** "Mentoria", "Networking", "Espaço Físico (coworking)".

`preferencia_segmento`

- **Significado:** Indica se um investidor ou programa tem preferência por algum segmento de atuação específico.

`contato_divulgacao_cientifica`

- **Significado:** O contato do setor ou pessoa responsável pela divulgação científica.
- **Contexto/Exemplo:** Relevante para ICTs e Universidades.
