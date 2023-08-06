from cloudshell.cp.core.utils import generate_ssh_key_pair


def test_generate_ssh_key_pair():
    private, public = generate_ssh_key_pair()
    assert "BEGIN RSA PRIVATE KEY" in private
    assert "END RSA PRIVATE KEY" in private
    assert public.startswith("ssh-rsa ")
