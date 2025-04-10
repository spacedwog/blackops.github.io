class BlackboardValidator:
    trusted_logins = {"admin123", "user456", "dev789"}  # exemplo
    trusted_domains = {"trusted-domain.com", "secure.org"}

    @staticmethod
    def validar_usuario(user_data, login_input: str) -> bool:
        """
        Valida se o usuário logado no GitHub corresponde ao login digitado
        ou pertence a uma lista confiável de logins/domínios.
        """
        if not user_data:
            return False  # ou logar erro, dependendo do que deseja

        login = (user_data.get("login") or "").lower()
        email = (user_data.get("email") or "").lower()

        # Validação por login exato ou início
        if login.startswith(login_input.lower()):
            return True

        # Validação por lista de logins confiáveis
        if login in BlackboardValidator.trusted_logins:
            return True

        # Validação por domínio de e-mail confiável
        if any(email.endswith("@" + domain) for domain in BlackboardValidator.trusted_domains):
            return True

        return False