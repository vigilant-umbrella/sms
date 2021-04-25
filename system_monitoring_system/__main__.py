import cli
import fire
import gui
import monitoring
import report


if __name__ == '__main__':
    commands = {
        '--summary': cli.summary,
        '--cpu': cli.cpu,
        '--memory': cli.memory,
        '--process': cli.process,
        '--storage': cli.storage,
        '--network': cli.network,
        '--misc': cli.misc,
        '--show-limit': cli.show_limit,
        '--update-limit': cli.update_limit,
        '--show-email': cli.show_email,
        '--update-email': cli.update_email,
        '--update-password': cli.update_password,
        '--send-email': cli.send_email,
        '--down-report': report.down_report,
        '--start-monitoring': monitoring.start,
        '--gui': gui.main,
        '-S': cli.summary,
        '-c': cli.cpu,
        '-M': cli.memory,
        '-p': cli.process,
        '-s': cli.storage,
        '-n': cli.network,
        '-m': cli.misc,
        '-g': gui.main
    }

    fire.Fire(commands)
