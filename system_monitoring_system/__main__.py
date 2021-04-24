import cli
import fire
import gui
import monitoring
import report


if __name__ == '__main__':
    commands = {
        '--summary': cli.summary,
        '-S': cli.summary,
        '--cpu': cli.cpu,
        '-c': cli.cpu,
        '--memory': cli.memory,
        '-M': cli.memory,
        '--process': cli.process,
        '-p': cli.process,
        '--storage': cli.storage,
        '-s': cli.storage,
        '--network': cli.network,
        '-n': cli.network,
        '--misc': cli.misc,
        '-m': cli.misc,
        '--show-limit': cli.show_limit,
        '--update-limit': cli.update_limit,
        '--show-email': cli.show_email,
        '--update-email': cli.update_email,
        '--update-password': cli.update_password,
        '--send-email': cli.send_email,
        '--down-report': report.down_report,
        '--start-monitoring': monitoring.start,
        '--gui': gui.main,
        '-g': gui.main
    }

    fire.Fire(commands)
