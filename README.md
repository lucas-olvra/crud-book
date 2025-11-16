Fluxo Completo da Aplicação

CLIENT (Postman/Frontend)
    |
    | POST /books (JSON)
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 1️⃣ RESOURCE/CONTROLLER (book_resource.py)                   │
│ - Recebe a requisição HTTP                                  │
│ - Valida o JSON (Pydantic faz isso automaticamente)        │
│ - Cria a conexão com o banco (Depends)                     │
│ - Chama o SERVICE                                           │
└─────────────────────────────────────────────────────────────┘
    |
    | CreateBookRequest (schema validado)
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 2️⃣ SERVICE (book_service.py)                                │
│ - Recebe o REQUEST (schema)                                │
│ - Converte REQUEST → DOMAIN (usando Mapper)                │
│ - Chama o DATAPROVIDER para salvar                         │
│ - Converte DOMAIN → RESPONSE (usando Mapper)               │
│ - Retorna o RESPONSE para o Resource                       │
└─────────────────────────────────────────────────────────────┘
    |
    | Book (objeto de domínio)
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 3️⃣ DATAPROVIDER (book_provider.py)                          │
│ - Recebe o objeto DOMAIN (Book)                            │
│ - Converte DOMAIN → DICT (usando Mapper)                   │
│ - Executa o SQL no banco de dados                          │
│ - Recebe a ROW do banco                                     │
│ - Converte ROW → DOMAIN (usando Mapper)                    │
│ - Retorna o DOMAIN para o Service                          │
└─────────────────────────────────────────────────────────────┘
    |
    | Book (com ID gerado pelo banco)
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 4️⃣ MAPPER (book_mapper.py)                                  │
│ - Faz TODAS as conversões entre camadas:                   │
│   • REQUEST → DOMAIN                                        │
│   • DOMAIN → DICT (para SQL)                               │
│   • ROW → DOMAIN (do banco)                                │
│   • DOMAIN → RESPONSE                                       │
└─────────────────────────────────────────────────────────────┘
Diagrama Simplificado
REQUEST → RESOURCE → SERVICE → DATAPROVIDER → DATABASE
   ↓         ↓          ↓           ↓             ↓
 (JSON)   (valida)  (lógica)    (persiste)    (salva)
                        ↓           ↓
                    MAPPER ←→ MAPPER
                        ↓           ↓
DATABASE → DATAPROVIDER → SERVICE → RESOURCE → RESPONSE
   ↓             ↓          ↓          ↓          ↓
(retorna)    (converte)  (processa) (retorna)  (JSON)

Resumo de Responsabilidades
Camada        O que faz                          O que NÃO faz
RESOURCE      Recebe HTTP, valida, retorna HTTP  Não conhece banco de dados
SERVICE       Orquestra a lógica de negócio      Não conhece SQL
DATAPROVIDER  Fala com o banco de dados          Não conhece HTTP
MAPPER        Converte entre formatos            Não tem lógica de negócio
DOMAIN        Representa a entidade Book         Não tem comportamento
SCHEMA        Define contratos de entrada/saída  Não persiste dados

Como pensar ao criar um endpoint novo
Quando você for criar um novo endpoint, pense de fora para dentro:

1️⃣ Comece pelo RESOURCE (a porta de entrada)
python@router.get("/{book_id}")
async def get_book(book_id: int):
    # O que eu preciso receber? → book_id
    # O que eu preciso retornar? → BookResponse
2️⃣ Depois pense no SERVICE (a lógica)
pythonasync def get_book(self, book_id: int) -> BookResponse:
    # Qual a regra de negócio?
    # - Buscar o livro
    # - Se não existir, lançar exceção
    # - Converter para response
3️⃣ Depois o DATAPROVIDER (o banco)
pythonasync def get_book_by_id(conn, book_id: int) -> Book:
    # Qual o SQL?
    # SELECT * FROM books WHERE id = %s
4️⃣ Por fim, o MAPPER (as conversões)

Dica Final
- Sempre pense no fluxo:

- O que entra? (JSON → Schema)
- O que fazer? (Service)
- Onde salvar/buscar? (DataProvider)
- O que retornar? (Schema)

E o Mapper é o "tradutor" entre todas essas camadas!

Veja o diagrama completo do sistema no Excalidraw:
[Diagrama Excalidraw](https://excalidraw.com/#json=tonx4Kyex7NxfKLsaYVG9,wPQNrzptp9C_beSf4YENdg)