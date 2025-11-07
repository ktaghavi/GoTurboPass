# Database Backup & Restore

PostgreSQL backup and restore procedures for GoTurboPass.

---

## 1. Backup Database

### Full Database Dump

```bash
pg_dump -U postgres -d goturbopass -F c -b -v -f backups/goturbopass_$(date +%Y%m%d_%H%M%S).dump
```

**Flags**:
- `-U postgres`: Username
- `-d goturbopass`: Database name
- `-F c`: Custom compressed format
- `-b`: Include large objects
- `-v`: Verbose output
- `-f`: Output file

### Plain SQL Dump (human-readable)

```bash
pg_dump -U postgres -d goturbopass > backups/goturbopass_$(date +%Y%m%d_%H%M%S).sql
```

### Schema Only (no data)

```bash
pg_dump -U postgres -d goturbopass --schema-only > backups/schema_$(date +%Y%m%d_%H%M%S).sql
```

### Data Only (no schema)

```bash
pg_dump -U postgres -d goturbopass --data-only > backups/data_$(date +%Y%m%d_%H%M%S).sql
```

---

## 2. Restore Database

### From Custom Dump (`.dump`)

```bash
pg_restore -U postgres -d goturbopass -v backups/goturbopass_20251107_120000.dump
```

### From SQL Dump (`.sql`)

```bash
psql -U postgres -d goturbopass < backups/goturbopass_20251107_120000.sql
```

### Create Fresh Database Before Restore

```bash
# Drop existing database (WARNING: Deletes all data!)
psql -U postgres -c "DROP DATABASE goturbopass;"

# Create new database
psql -U postgres -c "CREATE DATABASE goturbopass;"

# Restore from backup
pg_restore -U postgres -d goturbopass -v backups/goturbopass_20251107_120000.dump
```

---

## 3. Automated Backups (Cron)

### Daily Backup Script

Create `scripts/backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/goturbopass"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U postgres -d goturbopass -F c -b -f $BACKUP_DIR/goturbopass_$TIMESTAMP.dump

# Delete backups older than retention period
find $BACKUP_DIR -name "goturbopass_*.dump" -mtime +$RETENTION_DAYS -delete

echo "Backup completed: goturbopass_$TIMESTAMP.dump"
```

Make executable:
```bash
chmod +x scripts/backup.sh
```

### Add to Crontab (Daily at 2 AM)

```bash
crontab -e
```

Add line:
```
0 2 * * * /path/to/GoTurboPass/scripts/backup.sh >> /var/log/goturbopass_backup.log 2>&1
```

---

## 4. Backup Best Practices

### Storage
- Store backups on separate physical disk/server
- Use cloud storage (S3, Google Cloud Storage) for off-site redundancy
- Encrypt backups at rest (use `pgcrypto` or filesystem encryption)

### Retention Policy
- **Daily backups**: Keep for 30 days
- **Weekly backups**: Keep for 3 months
- **Monthly backups**: Keep for 1 year

### Testing
- Test restores monthly to ensure backups are valid
- Verify data integrity after restore

### Security
- Restrict backup file permissions: `chmod 600 backups/*.dump`
- Never commit backups to version control
- Add `backups/` to `.gitignore`

---

## 5. Disaster Recovery

### Recovery Time Objective (RTO)
- Target: < 2 hours from failure to operational

### Recovery Point Objective (RPO)
- Target: < 24 hours of data loss (daily backups)

### Recovery Steps

1. **Identify failure type**:
   - Data corruption
   - Accidental deletion
   - Hardware failure
   - Security breach

2. **Stop application** (prevent further damage):
   ```bash
   # Stop backend
   pkill -f "python app.py"
   ```

3. **Assess latest valid backup**:
   ```bash
   ls -lh backups/
   ```

4. **Restore from backup** (see section 2)

5. **Verify data integrity**:
   ```bash
   psql -U postgres -d goturbopass
   SELECT COUNT(*) FROM users;
   SELECT COUNT(*) FROM modules;
   ```

6. **Restart application**:
   ```bash
   make dev
   ```

---

## 6. Point-in-Time Recovery (PITR)

For production, enable **Write-Ahead Logging (WAL)** archiving:

### Enable WAL Archiving

Edit `postgresql.conf`:
```
wal_level = replica
archive_mode = on
archive_command = 'cp %p /var/backups/goturbopass/wal/%f'
```

Restart PostgreSQL:
```bash
sudo systemctl restart postgresql
```

### Restore to Specific Time

```bash
pg_restore -U postgres -d goturbopass --target-time "2025-11-07 12:00:00" backups/goturbopass.dump
```

---

## 7. Monitoring

### Backup Size Monitoring

```bash
du -sh backups/
```

### Backup Age Check

```bash
find backups/ -name "*.dump" -mtime -1
```

If no files found, last backup is > 24 hours old (alert!)

---

## 8. Emergency Contacts

**Database Admin**: Kamyar Taghavi (placeholder)
**Email**: db-admin@goturbopass.com
**Phone**: (555) 123-4567

---

## 9. Appendix: PostgreSQL Connection

### Local Connection

```bash
psql -U postgres -d goturbopass
```

### Remote Connection

```bash
psql -h <host> -U postgres -d goturbopass -p 5432
```

### Connection String

```
postgresql://postgres:password@localhost:5432/goturbopass
```

---

## Notes

- Always test backups in staging environment first
- Document all restore operations in incident log
- Review backup strategy quarterly
