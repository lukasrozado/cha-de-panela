# Chá de Panela - Lukas e Raphaela

Site estático hospedado no GitHub Pages para confirmação de presença e reserva de presentes. O frontend é um HTML/CSS/JS simples (Tailwind CSS via CDN) e o backend é um Google Apps Script que lê/grava em planilhas Google (Google Sheets) e envia notificações por e-mail.

---

- **index.html**: página única com seções de landing, confirmação de presença, lista de presentes, endereço e outras informações. Contém JS que faz JSONP GET no Apps Script e formulários POST para reserva/confirmar.
- **static/images/**: todas as imagens referenciadas. Os nomes dos arquivos devem ser “slug” do nome do item:
  - Minúsculo, sem acentos, espaços e caracteres especiais substituídos por hífen.
  - Exemplo: `"Aspirador de pó electrolux vertical e portátil"` → `aspirador-de-po-electrolux-vertical-e-portatil.jpg`.

---

## ⚙️ Configuração do Google Sheets e Apps Script

1. **Planilha Google Sheets**:
   - Crie (ou use a existente) com ID visível na URL.
   - Aba **“Reservas”**: linha 1 (cabeçalho) exatamente:  
     ```
     Timestamp | item | nome | celular
     ```
   - Aba **“Confirmacoes”**: linha 1:  
     ```
     Timestamp | nome | celular | confirmacao
     ```
   - Compartilhe apenas se desejar; o Apps Script executa como sua conta.

2. **Apps Script**:
   - Em https://script.google.com, crie novo projeto vinculado à planilha.
   - Cole o código `Code.gs` fornecido (doGet JSONP, doPost com redirecionamento HTML). Ajuste:
     - `SHEET_ID` igual ao ID da planilha.
     - `EMAIL_DESTINO` (se desejar notificação via e-mail).
     - `BASE_URL` igual à URL do GitHub Pages (ex: `https://seuusuario.github.io/seurepo/`).
   - Remova chamadas a `.setHeader(...)`.
   - Salve e **implante como Web App**:
     - “Executar como”: Você.
     - “Quem tem acesso”: Qualquer pessoa, mesmo anônima.
   - Copie a URL do Web App (ex: `https://script.google.com/macros/s/AKfycbzEO2Y0lHaDHWQ6A4-DGPHYLg3OcWRAVrGLiU4oo32PXtZE3T6dlPUca4qu2e2qctyC/exec`).

3. **Verificações iniciais**:
   - Teste GET manual: abra no navegador `...?callback=handleReservations`. Deve retornar chamada JS com array (inicialmente vazio).
   - Teste POST manual (via formulário do site): reserve um item. Planilha deve ganhar linha e e-mail (se ativado). Redirecione de volta com `?reservado=true#presentes`.
   - Apague linhas de teste na planilha para resetar.

---

## 🚀 Deploy do Frontend (GitHub Pages)

1. No repositório GitHub, commit de `index.html` e pasta `static/images/`.
2. Em **Settings > Pages**, selecione branch (`main` ou outra) e pasta (`/ (root)` ou `/docs` se usar).
3. Aguarde publicação; URL será `https://<seu-usuario>.github.io/<seu-repo>/`.
4. Acesse e teste:
   - Carregamento inicial: todos os cards aparecem (JSONP GET retorna `[]`).
   - Reserve um item: botão/form submete, grava na planilha, e ao recarregar aparece “Reservado” no card.
   - Para liberar: apague a linha na planilha e recarregue.

---

## ✏️ Como adicionar/remover itens (cards)

1. **Adicionar novo item**:
   - **Imagem**: coloque o arquivo em `static/images/`, com nome slug correspondente ao texto exato do item.
   - **Card no HTML**: no `<section id="presentes">`, dentro da `<div class="grid ...">`, adicione um bloco:
     ```html
     <div class="text-center border p-4 bg-white rounded shadow card-item" data-item="Nome Exato do Item">
       <img src="static/images/slug-do-item.jpg" alt="Nome Exato do Item" width="300" height="300" class="mx-auto mb-2">
       <p class="mb-2 font-semibold">Nome Exato do Item</p>
       <form class="space-y-2 form-reserva"
             action="URL_DO_WEBAPP"
             method="post">
         <input type="hidden" name="item" value="Nome Exato do Item">
         <input type="text" name="nome" placeholder="Seu nome" required class="border p-2 rounded w-full">
         <input type="tel" name="celular" placeholder="Seu celular" required class="border p-2 rounded w-full">
         <button type="submit" class="border px-4 py-2 w-full bg-green-600 text-white rounded hover:bg-green-700">Reservar</button>
       </form>
     </div>
     ```
   - Garanta que o valor em `data-item="Nome Exato do Item"` e `<input name="item" value="Nome Exato do Item">` coincida exatamente com o texto comparado no Apps Script.
   - Commit/push e aguarde atualização do GitHub Pages.

2. **Remover item**:
   - Exclua o bloco `<div class="card-item"...>` correspondente e, se quiser, delete imagem em `static/images/`.
   - Commit/push e aguarde.

---

## 🧪 Testes e limpeza

- **Testar reserva**: preencha formulário de um card; verifique planilha, e-mail e que o card mostra “Reservado”.
- **Testar duplicata**: tente reservar o mesmo item novamente; deve redirecionar com mensagem “Item já reservado”.
- **Limpar reservas**: abra o Google Sheets e delete linhas de teste (mantendo cabeçalho). No site, recarregue e os cards voltam ao estado inicial.
- **Testar confirmação de presença**: abra seção “Confirmação de presença”, submeta; verifique aba “Confirmacoes” e mensagem de sucesso; delete linha de teste para resetar.

---

## ⚙️ Configurações importantes

- **URL do Web App**: no `index.html` e no Apps Script (`BASE_URL`), use a URL exata obtida ao implantar. Se reimplantar, atualize.
- **Permissões**: se Web App der erro de autorização, reimplante confirmando “Qualquer pessoa, mesmo anônima” e autorize acesso ao Sheets e MailApp.
- **Quotas de e-mail**: MailApp tem limite diário (~100 e-mails). Para múltiplos testes, você pode:
  - Temporariamente comentar ou desabilitar `MailApp.sendEmail(...)` no Apps Script.
  - Usar outro e-mail de teste.
- **CORS**: usamos JSONP para GET e formulários HTML para POST. Não há fetch direto.
- **Cache**: GitHub Pages pode demorar alguns minutos para atualizar após push; use Ctrl+F5 para forçar recarregamento.
- **Timezones**: Apps Script grava `new Date()` com fuso da conta Google. Se precisar mostrar no frontend, converta manualmente.
- **Logs**: no editor Apps Script, use “Executions” ou `Logger.log()` para depurar.

---

## 📖 Documentação extra

- [Google Apps Script: ContentService JSONP](https://developers.google.com/apps-script/guides/content#json-p)
- [GitHub Pages Basics](https://docs.github.com/en/pages/getting-started-with-github-pages)
- [Tailwind CSS via CDN](https://tailwindcss.com/docs/installation/play-cdn)

---
