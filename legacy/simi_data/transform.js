const fs = require("fs");
const data = require("./simi_data.js");

// Mapa de renomeação
const renameMap = {
  "Cadastro aprovado?": "cadastro_aprovado",
  "Você concorda em divulgar as informações inseridas neste formulário em estudos sobre o ecossistema de inovação de Minas Gerais e na plataforma do SIMI?":
    "autorizacao_divulgacao",
  "Qual o nome da sua organização?": "nome_organizacao",
  "Em qual cidade está a sede da organização?": "cidade_sede",
  "Em qual estado (UF) está a sede da organização?": "uf_sede",
  "Qual o link com o logo da organização?": "logo_url",
  "Descrição da organização": "descricao_organizacao",
  "Qual o site da organização?": "site_organizacao",
  "Qual o melhor e-mail para contato?": "email_contato",
  "Em qual categoria sua organização se enquadra?": "categoria_organizacao",
  "Qual fase de investimentos que está captando?": "fase_investimento_busca",
  "Qual(is) incentivo(s) fiscal(is) o município possui para o desenvolvimento de empresas de base tecnológica?":
    "incentivos_fiscais_municipio",
  "Qual departamento (secretaria, subsecretaria, diretoria, assessoria, etc) é responsável pela pauta/temática de Ciência, Tecnologia e Inovação?":
    "orgao_responsavel_cti",
  "Qual o tipo de organização?": "tipo_organizacao",
  "Caso sua organização possua um setor ou pessoa responsável por divulgação científica, informe o contato":
    "contato_divulgacao_cientifica",
  "A organização possui um NIT (Núcleo de Inovação Tecnológica) ou departamento responsável por propriedade intelectual e transferências tecnológicas?":
    "possui_nit",
  "Quais são as principais áreas do conhecimento em que a organização possui expertise?":
    "areas_expertise",
  "Qual a tese de investimento da organização?": "tese_investimento",
  "Em quantas startups a organização já investiu?": "num_startups_investidas",
  Segmento: "segmento_atuacao",
  "Programas de desenvolvimento": "programas_desenvolvimento",
  "Modelo de negócio": "modelo_negocio",
  "Tecnologia disruptiva": "tecnologias_disruptivas",
  "Segmentação de clientes": "segmentacao_clientes",
  "Fase de negócio": "fase_negocio",
  "Número de funcionários": "numero_funcionarios",
  "Fase de investimentos captada/fornecida": "fase_investimento_captada",
  "Está buscando investimento?": "busca_investimento",
  Linkedin: "linkedin_url",
  "Preferência relativa ao perfil/segmento": "preferencia_segmento",
  "Benefícios dados pelo programa": "beneficios_programa",
  "Investimento médio por startup": "investimento_medio_startup",
  "Exige equity?": "exige_equity",
};

// Função de transformação
function transformData(entry) {
  const newEntry = {};

  for (const [key, value] of Object.entries(entry)) {
    if (renameMap.hasOwnProperty(key)) {
      newEntry[renameMap[key]] = value;
    } else {
      console.log("Chave não mapeada:", key);
      newEntry[key] = value;
    }
  }

  return newEntry;
}

// Transformar todos os dados
const transformedData = data.map((entry) => {
  return transformData(entry);
});

// Escrever o novo arquivo JSON
fs.writeFileSync(
  "transformed_simi_data.json",
  JSON.stringify(transformedData, null, 2),
  "utf-8"
);
