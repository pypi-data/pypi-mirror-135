from copydetect import CopyDetector

detector = CopyDetector(code1='from copydetect import CopyDetector detector = CopyDetector(test_dirs=["tests"], extensions=["py"], display_t=0.5)',
                        code2='detector.add_file("copydetect/utils.py")>>> detector.run()0.00: Generating file fingerprints>>> detector.generate_html_report()Output saved to report/report.html', 
                        extension="python", display_t=0.1)
detector = detector.run()


