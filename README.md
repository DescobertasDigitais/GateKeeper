# GateKeeper
![banner](https://files.catbox.moe/se1gwu.png)
![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Um scanner de portas avançado escrito em Python que permite verificar rapidamente portas abertas em um host alvo, com suporte para varredura multi-threaded e identificação de serviços.

## Recursos Principais

- 🚀 **Varredura rápida** com multi-threading (até 500+ threads)
- 🔍 **Identificação automática de serviços** com banco de banners conhecidos
- 🎨 **Saída colorida** para melhor legibilidade
- 📊 **Relatório detalhado** com estatísticas de tempo e resultados
- ⚙️ **Suporte para intervalos de portas** (ex: 20-25,80,443,1000-2000)
- 🌐 **Resolução de hostnames** para endereços IP
- ⏱️ **Timeout configurável** para conexões

## Instalação

1. Certifique-se de ter Python 3.6 ou superior instalado:
   ```bash
   python3 --version
   ```

2. Clone o repositório ou baixe o script:
   ```bash
   git clone https://github.com/DescobertasDigitais/GateKeeper.git
   cd GateKeeper
   ```

3. (Opcional) Recomenda-se usar um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate    # Windows
   ```

## Uso Básico

```bash
python3 gatekeeper.py <target> [-p PORTAS] [-t THREADS] [-T TIMEOUT]
```

### Argumentos

| Argumento   | Descrição                                  | Padrão     |
|-------------|--------------------------------------------|------------|
| `target`    | IP ou hostname do alvo                     | Obrigatório|
| `-p, --ports` | Portas para escanear (ex: 80,443,20-25)  | 1-1024     |
| `-t, --threads` | Número de threads para usar             | 100        |
| `-T, --timeout` | Timeout de conexão em segundos          | 1.0        |

### Exemplos

1. **Varredura básica** das portas comuns:
   ```bash
   python3 gatekeeper.py 192.168.1.1
   ```

2. **Portas específicas**:
   ```bash
   python3 gatekeeper.py example.com -p 22,80,443
   ```

3. **Intervalo de portas** com mais threads:
   ```bash
   python3 gatekeeper.py 192.168.1.100 -p 1-1024 -t 200
   ```

4. **Timeout personalizado** para conexões lentas:
   ```bash
   python3 gatekeeper.py 192.168.1.1 -T 2.0
   ```

## Saída de Exemplo

```
[*] Iniciando varredura em 192.168.1.1...
[*] Escaneando 1024 portas com 100 threads

Resultados da varredura para 192.168.1.1:
Tempo total: 12.34 segundos
Portas escaneadas: 1024
Portas abertas: 3

PORTA    SERVIÇO
-----    -------
22       SSH (SSH-2.0-OpenSSH_7.9p1)
80       HTTP (HTTP/1.1 200 OK...)
443      HTTPS (HTTP/1.1 200 OK...)
```

## Serviços Reconhecidos

O scanner reconhece automaticamente os seguintes serviços com base nas portas padrão:

- FTP (21)
- SSH (22)
- Telnet (23)
- SMTP (25)
- DNS (53)
- HTTP (80)
- POP3 (110)
- IMAP (143)
- HTTPS (443)
- MySQL (3306)
- RDP (3389)
- VNC (5900)
- HTTP-Alt (8080)

Para portas não listadas, será exibido "Serviço desconhecido".

## Boas Práticas

1. **Permissão**: Sempre obtenha permissão antes de escanear sistemas que não são de sua propriedade.
2. **Threads**: Ajuste o número de threads conforme a capacidade da sua rede e do alvo.
3. **Timeout**: Aumente o timeout para redes mais lentas ou hosts com restrições.
4. **Portas**: Para varreduras completas, use intervalos como `1-65535`.

## Limitações

- Não realiza escaneamento UDP, apenas TCP
- Depende da resposta do serviço para identificação precisa
- Varreduras muito agressivas podem ser bloqueadas por firewalls

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Autor

[Descobertas Digitais](https://github.com/DescobertasDigitais) - Desenvolvedor

---

**Aviso Legal**: Este software é apenas para fins educacionais e de teste de segurança autorizado. O uso não autorizado contra sistemas sem permissão explícita é ilegal.
