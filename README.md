# my_own_collection

## Домашнее задание к занятию 6 «Создание собственных модулей»

**Выполнил:** DudnikovDaniil

---

## 1. Описание работы

В рамках домашнего задания создана Ansible коллекция `my_own_namespace.yandex_cloud_elk`, содержащая пользовательский модуль `my_own_module`.

### 1.1 Функциональность модуля

Модуль `my_own_module` предназначен для создания текстового файла на удалённом хосте. Он принимает два обязательных параметра:
- `path` — абсолютный путь к создаваемому файлу;
- `content` — содержимое, которое будет записано в файл.

Модуль поддерживает режим проверки (check mode) и обеспечивает идемпотентность: при повторном запуске с теми же параметрами изменений не производится, если файл уже существует и его содержимое совпадает с указанным.

### 1.2 Пример использования

```bash
- name: Create a test file
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/test.txt
    content: "Hello, World!"
```

---

## 2. Структура коллекции

```bash
my_own_collection/
├── my_own_namespace/
│   └── yandex_cloud_elk/
│       ├── galaxy.yml
│       ├── README.md
│       ├── meta/
│       │   └── runtime.yml
│       ├── plugins/
│       │   └── modules/
│       │       └── my_own_module.py
│       ├── roles/
│       │   └── test_module_role/
│       │       ├── defaults/
│       │       │   └── main.yml
│       │       └── tasks/
│       │           └── main.yml
│       └── playbook.yml
├── screenshots/
│   ├── step4-module-check.png
│   ├── step6-idempotenc1.png
│   ├── step6-idempotenc2.png
│   ├── step15-collection-install.png
│   └── step16-playbook-run.png
├── README.md
└── my_own_namespace-yandex_cloud_elk-1.0.0.tar.gz
```

---

## 3. Ссылки для сдачи

| Что сдаётся | Ссылка |
|-------------|--------|
| Коллекция на GitHub | https://github.com/DudnikovDaniil/my_own_collection |
| .tar.gz архив | https://github.com/DudnikovDaniil/my_own_collection/raw/main/my_own_namespace-yandex_cloud_elk-1.0.0.tar.gz |

---

## 4. Выполнение этапов задания

### 4.1 Пункт 4 — проверка модуля локально

Была выполнена проверка синтаксиса модуля с помощью команды:

```bash
python -m py_compile my_own_module.py
```

Результат: ошибок не обнаружено, модуль готов к использованию.

**Скриншот:** `screenshots/step4-module-check.png`

---

### 4.2 Пункт 6 — проверка идемпотентности

Был написан тестовый playbook `test_playbook.yml`, который однократно создаёт файл `/tmp/ansible_test.txt` с содержимым.

**Первый запуск** (файл отсутствует):

Результат: `changed=1` — файл успешно создан.

**Второй запуск** (файл уже существует):

Результат: `changed=0` — изменений не произошло, идемпотентность соблюдена.

**Скриншоты:**
- `screenshots/step6-idempotenc1.png` (первый запуск)
- `screenshots/step6-idempotenc2.png` (второй запуск)

---

### 4.3 Пункт 15 — установка коллекции из архива

Коллекция была собрана в архив командой:

```bash
ansible-galaxy collection build
```

После чего установлена из локального `.tar.gz` файла:

```bash
ansible-galaxy collection install my_own_namespace-yandex_cloud_elk-1.0.0.tar.gz --force
```

Результат: коллекция успешно установлена в систему.

**Скриншот:** `screenshots/step15-collection-install.png`

---

### 4.4 Пункт 16 — запуск playbook после установки

После установки коллекции был выполнен playbook `test.yml`, использующий модуль из установленной коллекции:

```bash
- name: Test installed collection
  hosts: localhost
  tasks:
    - name: Create file via collection module
      my_own_namespace.yandex_cloud_elk.my_own_module:
        path: /tmp/collection_test.txt
        content: "Installed from collection archive!"
```

Результат: `changed=1` — модуль отработал корректно, файл создан.

**Скриншот:** `screenshots/step16-playbook-run.png`

---

## 5. Сводная таблица результатов

| Этап | Описание | Результат |
|------|----------|-----------|
| Пункт 4 | Проверка синтаксиса модуля | Успешно |
| Пункт 6 (первый запуск) | Создание файла | changed=1 |
| Пункт 6 (второй запуск) | Проверка идемпотентности | changed=0 |
| Пункт 15 | Установка коллекции из архива | Успешно |
| Пункт 16 | Запуск playbook после установки | changed=1 |

---

## 6. Теги

В репозитории создан тег `1.0.0`, соответствующий первому релизу коллекции.

```bash
git tag -a 1.0.0 -m "First release of collection"
git push --tags
```

---
