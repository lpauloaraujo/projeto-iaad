![mongodb logo](Mongodb.png)

## 📌 Processo de instalação do MongoDb + MongoDB Compass?

1. Acesse o site www.mongodb.com

![install 1](Install1.png)

2. Clique em "Produtos" no menu superior e depois clique em "Community Edition".

![install 2](Install2.png)

3. Role a tela e clique em "Download".

![install 3](Install3.png)

4. Clique em "Next".

![install 4](Install4.png)

5. Aceite os termos no Acordo de Licença e clique em "Next".

![install 5](Install5.png)

6. Clique em "Complete".

![install 6](Install6.png)

7. Clique em "Next".

![install 7](Install7.png)

8. Marque a opção "Install MongoDB Compass" e clique em "Next".

![install 8](Install8.png)

9. Por fim clique em "Install".

![install 9](Install9.png)


## 📌 Como o mongodb armazena os dados?

![mongodb works](Mongodbworks.png)

## 📌 Como os relacionamentos funcionam no MongoDB?

Diferente de um banco relacional, onde os relacionamentos são mantidos por chaves primárias e estrangeiras distribuídas entre tabelas, no MongoDB existem duas formas principais de estruturar relacionamentos:

### Documentos Incorporados (Embedded Documents)
Os dados relacionados são armazenados dentro de um mesmo documento.

**Exemplo:** No nosso banco, os programadores estão dentro das startups e os dependentes dentro dos programadores.
- 🚀 **Vantagem:** Acesso rápido e eficiente aos dados relacionados sem necessidade de joins.
- ⚠️ **Desvantagem:** Pode gerar documentos muito grandes, tornando atualizações mais complexas.

### Referências entre documentos (Normalization via References)
Os relacionamentos são feitos por meio do armazenamento de IDs de documentos externos.

**Exemplo:** Em vez de armazenar os programadores dentro das startups, poderíamos ter uma coleção separada de programadores, cada um com um campo `startup_id` referenciando a startup à qual pertence.
- 🔗 **Vantagem:** Evita duplicação e facilita atualização de dados.
- 🔄 **Desvantagem:** Requer lookups para buscar informações de diferentes coleções.
