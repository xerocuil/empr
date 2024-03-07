# Changelog

## To-Do

- [ ] Settings
- [ ] Package management
    - [X] FTP Server
    - [x] Install scripts
    - [x] Package upload scripts
    - [ ] Replace alert in uninstall script

- [x] Import legacy media
- [ ] Remove legacy elements from models
- [ ] Forms
    + [x] SQLite*
    + [ ] JSON
- [ ] API 
    - [ ] Host platforms sync
- [x] Create list tables
- [x] Pagination
- [x] Search
- [ ] UX
- [ ] Devices
    + [ ] Upload Config Form
    + [ ] Device Edit Form
- [x] Flash messaging
- [x] Add confirm to delete function

## Build 2024.0306

### Added

- Device support (install/remove)
- FTP server support
- Game list pagination
- Pywebview window management
- Javascript-based search function
- Single page readme for packages

### Changed

- Route management through Blueprint
- Migrated platform from Django to Flask
- Images managed via a flat-file system instead of database

## [0.3.1] - 2022.0814.2023

### Added

- `alt_title`, `engine` to Game model
- Platform logos to platform game index

## [0.3.0] 

### Added

- Loading screen
- App initializes database and app directories if not found
- Giantbomb, IGDB, ProtonDB to Links section on games.detail

### Changed

- Added `empr.py` to replace `manage.py` as main exec
- Platform is no longer a required field
- Changed browser engine to nativefier

### Removed

- Iron browser

## [0.2.0] - 2022.0812.2158

### Added

- Desktop support (Iron Browser)

### Changed

- Minor UI changes

## [0.1.0] - 2020.0811.2239

### Added
- Forms (Game, Genre, Platform, Tag) => add, edit, delete
- System messages

### Changed
- UI update
