init -990 python in mas_submod_utils:

    Submod(
        author="Bach",
        name="Steam Together",
        description="Steam Together allows your Monika to interact directly with your Steam library.{b}{color=#ef4444}[[DEMO]{/color}{/b}",
        version="0.0.2"
    )

init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Steam Together",
            user_name="bachxyh",
            tag_formatter=lambda v: v[1:].partition("-")[0],
            repository_name="mas-steamtogetherEN",
            extraction_depth=3
        )
