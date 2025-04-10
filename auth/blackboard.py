# auth/blackboard.py
class BlackboardValidator:
    @staticmethod
    def validar_usuario(user_data, login_input: str) -> bool:
        """
        Valida se o usuário logado no GitHub corresponde ao login digitado
        ou pertence a um domínio confiável.
        """
        login = user_data.get("login") or ""
        email = user_data.get("email") or ""

        if login.startswith(login_input):
            return True
        if "trusted-domain.com" in email:
            return True
        return False