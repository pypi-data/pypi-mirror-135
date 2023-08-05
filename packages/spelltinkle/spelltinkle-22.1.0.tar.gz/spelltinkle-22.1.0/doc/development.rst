Development
===========

Quick overview
--------------

::

    Configuration

    Screen

    Input

    Backup:
        session: Session

    Session:
        docs: List[Document]
        scr: Screen
        mail_clients: Dict[str, MailClient]
        folder, positions, lastsearchstring, lastkey, lasttime,
        memory, chars, failed, xclip

    Document:
        lines: List[str]
        session: Session
        view: View
        history: History
        color: Color
        completion: Completion
        handler: Optional[Input]
        modified, backup_needed, changes, path, timestamp, name, mode

    TextDocument(Document):
        insert_character()

    Completion

    Color

    History

    View

    Choise



Pygments + ...

bitbucket


Test coverage
-------------

::

    python3-coverage run --source=spelltinkle -m spelltinkle.test.selftest
