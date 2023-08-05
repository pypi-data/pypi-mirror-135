from inmanta.module import Project


def test_agent_config(project: Project):
    project.compile(
        """
        import ip

        host = ip::Host(
            name="test",
            ip="127.0.0.1",
            os=std::linux,
        )
    """
    )
    agent_config = project.get_resource("std::AgentConfig")
    assert not agent_config

    project.compile(
        """
        import ip

        host = ip::Host(
            name="test",
            ip="127.0.0.1",
            os=std::linux,
            remote_agent=true,
        )
    """
    )

    agent_config = project.get_resource("std::AgentConfig")
    assert agent_config
    assert agent_config.uri == "ssh://root@127.0.0.1:22?python=python"

    project.compile(
        """
        import ip

        host = ip::Host(
            name="test",
            ip="127.0.0.1",
            os=std::OS(name="testos", family=std::unix, python_cmd="test"),
            remote_agent=true,
        )
    """
    )

    agent_config = project.get_resource("std::AgentConfig")
    assert agent_config
    assert agent_config.uri == "ssh://root@127.0.0.1:22?python=test"
