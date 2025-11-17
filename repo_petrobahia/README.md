# PetroBahia S.A.

PetroBahia S.A. é uma empresa fictícia do setor de óleo e gás. O sistema interno calcula preços de combustíveis, valida clientes e gera relatórios operacionais. A base legada estava mal estruturada, com responsabilidades misturadas, duplicações e pouca aderência a boas práticas.

Este repositório traz uma refatoração orientada por PEP 8, Clean Code e princípios SOLID (SRP e OCP) para facilitar evolução e manutenção.

## Objetivos
- Melhorar a legibilidade e clareza do código
- Extrair funções e classes coesas
- Eliminar duplicações e efeitos colaterais inesperados
- Melhorar nomes, modularidade e pontos de extensão

## Estrutura
```
repo_petrobahia/
├── clientes.txt
├── main.py                  # Ponto de entrada da aplicação
├── src/
│   ├── legacy/                 # Código legado preservado apenas como referência
│   └── petrobahia/             # Implementação moderna da aplicação
│       ├── __init__.py
│       ├── customers.py        # Cadastro, validação e persistência de clientes
│       ├── discounts.py        # Estratégias de desconto por cupom
│       ├── models.py           # Dataclasses de domínio (Cliente e Pedido)
│       ├── orders.py           # Serviço de processamento de pedidos
│       ├── pricing.py          # Estratégias de precificação por produto
│       ├── repositories.py     # Persistência em arquivo (injeção via protocolo)
│       └── validators.py       # Validações e mensagens de erro/alerta
└── ...
```

## Como executar
1. Certifique-se de possuir Python 3.10 ou superior.
2. A partir da pasta `repo_petrobahia`, execute:
   ```bash
   python main.py
   ```
   O script mantém a mesma saída do programa legado, agora sustentada pela nova arquitetura.

## Decisões de design
- **Separação de responsabilidades (SRP):** clientes, pedidos, precificação, descontos e persistência ficaram em módulos próprios. Cada classe tem responsabilidade única e explicitada.
- **Pontos de extensão (OCP):** estratégias de preço (`PricingStrategy`) e descontos (`DiscountStrategy`) são injetadas e podem receber novas implementações sem alterar código existente.
- **Modelagem explícita:** `Customer` e `Order` são dataclasses, tornando parâmetros claros e evitando dicionários anônimos em todo o código.
- **Validação e mensagens consistentes:** o serviço de clientes centraliza mensagens de erro/aviso, mantendo compatibilidade com as mensagens do legado.

- **Persistência desacoplada:** repositórios seguem um protocolo simples (`CustomerRepository`), permitindo substituir o backend de armazenamento sem tocar na lógica de cadastro.
- **Compatibilidade preservada:** `main.py` imprime as mesmas mensagens observadas no legado, garantindo que relatórios ou integrações existentes continuem funcionando.

O código legado permanece no diretório `src/legacy` como referência histórica, mas a execução padrão utiliza apenas a nova camada modularizada.

## Mudanças implementadas e motivos
- **`main.py` posicionado na raiz** para seguir o layout padrão de projetos em modo `src/` e expor um ponto de entrada claro. O arquivo injeta o caminho de `src/` no `sys.path`, instancia serviços e mantém o fluxo original.
- **Pacote `src/petrobahia` criado** com módulos coesos:
  - `models.py`: centraliza as entidades `Customer` e `Order` em dataclasses imutáveis, reduzindo erros com dicionários soltos.
  - `validators.py`: concentra validações de campos obrigatórios e formato de email, preservando mensagens existentes.
  - `customers.py`: organiza o cadastro em um serviço que aplica validações, persiste o cliente e emite mensagens na mesma ordem do legado, agora direcionadas ao nome do cliente (fluxo de boas-vindas mais natural).
  - `repositories.py`: implementa um repositório de clientes baseado em arquivo, isolando a forma de persistência do restante da aplicação.
  - `pricing.py`: distribui as regras de precificação em estratégias específicas por produto, diminuindo condicionais encadeadas e facilitando extensões.
  - `discounts.py`: encapsula descontos por cupom em estratégias reutilizáveis, evitando `ifs` aninhados.
  - `orders.py`: coordena cálculo, descontos e arredondamento, devolvendo o mesmo resultado do legado e preparando o terreno para outros fluxos.
- **Arquivo `clientes.txt` movido para a raiz do projeto** (`repo_petrobahia/clientes.txt`) e leitura/gravação centralizada via repositório para evitar duplicação.
- **Remoção de `__pycache__` e inclusão no `.gitignore`** para manter o controle de versão limpo e alinhado às boas práticas de Python.
