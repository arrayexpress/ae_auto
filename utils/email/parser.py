__author__ = 'Ahmed G. Ali'


def geo_email_parse(email_body):
    ids = {}
    for word in email_body.split(" "):
        word = word.replace(',', '')
        if word.startswith('GSE'):
            geo_id = word
            ae_id = 'E-GEOD-%s' % word.replace('GSE', '')
            ids[geo_id] = ae_id
        elif word.startswith('GDS'):
            geo_id = word
            ae_id = 'E-GEOD-%s' % word.replace('GDS', '')
            ids[geo_id] = ae_id
    return ids

if __name__ == '__main__':
    email = u"""
[ Microarray OTRS ]	Ahmed Ali (ahmed@ebi.ac.uk) 2016-07-04 12:50:34
Logout
Logout
QueueView
QueueView
StatusView
StatusView
Phone-Ticket
Phone-Ticket
Email-Ticket
Email-Ticket
Search
Search
Customer
Customer
Bulk-Action
Bulk-Action
 -
Calendar
Calendar
Preferences
Preferences
Responsible (165)
Responsible (165)
Watched Tickets (0)
Watched Tickets (0)
New message (1)
New message (1)
Locked Tickets (1)
Locked Tickets (1)
Info	: You have 1 new message(s)!
[ Queue: developers::ahmed ]
Tickets shown: 1-50 - Page: 1 2 - Tickets available: 72 - All tickets: 73
Queues: My Queues (199) - annotare (42) - arrayexpress (19) - biosamples (15) - biostudies (1) - developers (186) - HTS new (19) - junk (5222) - miamexpress (1953) - raw (36866) - twitter (2)
ahmed (72) - atlas (77)

[ Ticket#: 1605090205 ] CRAM Spot Length Help	[ Age: 55 days 20 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-05-10 12:02:02
From:
Vadim Zalunin <vadim@ebi.ac.uk>
To:
datasubs@ebi.ac.uk, arrayexpress@ebi.ac.uk
Cc:
dsmirnov@ebi.ac.uk
Subject:
Re: CRAM Spot Length Help [Ticket#1605090205] (SUB#916874)
Hello,

For Illumina paired reads this is a valid approach unless the reads have
been trimmed or hard clipped.

Vadim

On 10/05/2016 11:40, datasubs@ebi.ac.uk wrote:
> Hi Ahmed,
>
> Dmitriy and/or Vadim are best suited to advise because the processing pipeline
> is already calculating these things from the submitted cram files. For Illumina
> output where forward and reverse reads are the same length you may be able to do
> something like this for spot length:
>
>> cramtools fastq -I LCK_1_10.cram | head -n2 | tail -n1 | wc -c
> 126
>
[...]
State:
open
Priority:
5 very high
Queue:
developers::ahmed
CustomerID:
Owner:
ahmed
Trac:
Curation_Status:

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 2015120910000291 ] Changing Release Date	[ Age: 207 days 21 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-01-08 10:02:03
From:
datasubs@ebi.ac.uk
To:
arrayexpress@ebi.ac.uk
Subject:
Re: [Ticket#2015120910000291] Changing Release Date (neilg) (SUB#907788)
Notes:
Ahmed: I've tested it using the same submission xml on the Webin test server and it is now working.
This should go to Amy to open the ticket for the Dev team to implement in AE.

Amy: Pivotal ticket logged ( https://www.pivotaltracker.com/story/show/86417364 ). Hope it'll be delivered soon! (25 Jan 2016)
Hi Ahmed,

The ability to update the hold date for a study has been added using the
HoldUntilDate attribute in the HOLD element in the submission XML.

Regards

Neil
Neil Goodgame
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.
State:
open
Priority:
4 high
Queue:
developers::ahmed
CustomerID:
Owner:
ahmed
Trac:
Curation_Status:

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1607040041 ] ENA (Webin-24): file processing errors	[ Age: 6 hours 48 minutes ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-07-04 06:02:02
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1607030294 ] ENA (Webin-24): file processing errors	[ Age: 1 day 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-07-03 06:02:02
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1607020563 ] [geo] GEO->AE unpublish notification: GSE67754 [NCBI trackin[..]	[ Age: 1 day 20 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-07-02 16:16:07
From:
"GEO - Emily Clough" <geo@ncbi.nlm.nih.gov>
To:
miamexpress@ebi.ac.uk
Subject:
[geo] GEO->AE unpublish notification: GSE67754 [NCBI tracking system #17956664[..]
------ MESSAGE BODY. YOU MAY CHANGE IT OR ADD COMMENTS ABOVE ------

Dear ArrayExpress Team,

The Series GSE67754 was returned to private status.

Regards,
The GEO Team
*************


---- END OF MESSAGE BODY.  PLEASE DO NOT CHANGE THE DATA BELOW ----
SK#:15:60:5:229:4334271

Please leave the subject line unchanged, and do not change the message
at end from the line with "END OF MESSAGE BODY" to the end.

NOTE: the geo email is often abused (spoofed) by spammers.  We never send
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	geo@ncbi.nlm.nih.g[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1607020545 ] ENA (Webin-24): file processing errors	[ Age: 2 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-07-02 06:03:17
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606280061 ] ENA (Webin-24): file processing errors	[ Age: 6 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-28 06:02:03
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606270036 ] ENA (Webin-24): file processing errors	[ Age: 7 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-27 06:02:02
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606260065 ] ENA (Webin-24): file processing errors	[ Age: 8 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-26 06:02:01
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606220125 ] ENA (Webin-24): file processing errors	[ Age: 12 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-22 06:02:02
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606210403 ] [geo] GEO->AE unpublish notification: GSE65169 [NCBI trackin[..]	[ Age: 12 days 22 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-21 14:14:11
From:
"GEO - Hyeseung Lee" <geo@ncbi.nlm.nih.gov>
To:
miamexpress@ebi.ac.uk
Subject:
[geo] GEO->AE unpublish notification: GSE65169 [NCBI tracking system #17943901[..]
------ MESSAGE BODY. YOU MAY CHANGE IT OR ADD COMMENTS ABOVE ------

Dear ArrayExpress Team,

The Series GSE65169 was returned to private status.

Regards,
The GEO Team

---- END OF MESSAGE BODY.  PLEASE DO NOT CHANGE THE DATA BELOW ----
SK#:15:60:5:227:1360630

Please leave the subject line unchanged, and do not change the message
at end from the line with "END OF MESSAGE BODY" to the end.

NOTE: the geo email is often abused (spoofed) by spammers.  We never send
encrypted messages or attachments unless agreed. We always sign emails by
name.
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	geo@ncbi.nlm.nih.g[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606210109 ] ENA (Webin-24): file processing errors	[ Age: 13 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-21 06:02:04
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606210065 ] [geo] GEO->AE unpublish notification: GSE71536 [NCBI trackin[..]	[ Age: 13 days 9 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-21 03:20:05
From:
"GEO - Patti Sherman" <geo@ncbi.nlm.nih.gov>
To:
miamexpress@ebi.ac.uk
Subject:
[geo] GEO->AE unpublish notification: GSE71536 [NCBI tracking system #17943092[..]
------ MESSAGE BODY. YOU MAY CHANGE IT OR ADD COMMENTS ABOVE ------

Dear ArrayExpress Team,

The Series GSE71536 was returned to private status.

Regards,
The GEO Team
*************


---- END OF MESSAGE BODY.  PLEASE DO NOT CHANGE THE DATA BELOW ----
SK#:15:60:5:222:4015098

Please leave the subject line unchanged, and do not change the message
at end from the line with "END OF MESSAGE BODY" to the end.

NOTE: the geo email is often abused (spoofed) by spammers.  We never send
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	geo@ncbi.nlm.nih.g[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606200334 ] [geo] GEO->AE unpublish notification: GSE74365 [NCBI trackin[..]	[ Age: 13 days 19 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-20 17:14:03
From:
"GEO - Patti Sherman" <geo@ncbi.nlm.nih.gov>
To:
miamexpress@ebi.ac.uk
Subject:
[geo] GEO->AE unpublish notification: GSE74365 [NCBI tracking system #17939672[..]
------ MESSAGE BODY. YOU MAY CHANGE IT OR ADD COMMENTS ABOVE ------

Dear ArrayExpress Team,

The Series GSE74365 was returned to private status.

Regards,
The GEO Team
*************


---- END OF MESSAGE BODY.  PLEASE DO NOT CHANGE THE DATA BELOW ----
SK#:15:60:5:225:1000312

Please leave the subject line unchanged, and do not change the message
at end from the line with "END OF MESSAGE BODY" to the end.

NOTE: the geo email is often abused (spoofed) by spammers.  We never send
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	geo@ncbi.nlm.nih.g[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606200129 ] [geo] GEO->AE unpublish notification: GSE83501 [NCBI trackin[..]	[ Age: 14 days 1 hour ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-20 11:28:03
From:
"GEO - Irene Kim" <geo@ncbi.nlm.nih.gov>
To:
miamexpress@ebi.ac.uk
Subject:
[geo] GEO->AE unpublish notification: GSE83501 [NCBI tracking system #17939075[..]
------ MESSAGE BODY. YOU MAY CHANGE IT OR ADD COMMENTS ABOVE ------

Dear ArrayExpress Team,

The Series GSE83501 was returned to private status.

Regards,
The GEO Team
*************

---- END OF MESSAGE BODY.  PLEASE DO NOT CHANGE THE DATA BELOW ----
SK#:15:60:5:217:2782673

Please leave the subject line unchanged, and do not change the message
at end from the line with "END OF MESSAGE BODY" to the end.

NOTE: the geo email is often abused (spoofed) by spammers.  We never send
encrypted messages or attachments unless agreed. We always sign emails by
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	geo@ncbi.nlm.nih.g[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606200111 ] [geo] GEO->AE unpublish notification: GSE83467 [NCBI trackin[..]	[ Age: 14 days 1 hour ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-20 11:28:03
From:
"GEO - Irene Kim" <geo@ncbi.nlm.nih.gov>
To:
miamexpress@ebi.ac.uk
Subject:
[geo] GEO->AE unpublish notification: GSE83467 [NCBI tracking system #17939074[..]
------ MESSAGE BODY. YOU MAY CHANGE IT OR ADD COMMENTS ABOVE ------

Dear ArrayExpress Team,

The Series GSE83467 was returned to private status.

Regards,
The GEO Team
*************

---- END OF MESSAGE BODY.  PLEASE DO NOT CHANGE THE DATA BELOW ----
SK#:15:60:5:228:4025240

Please leave the subject line unchanged, and do not change the message
at end from the line with "END OF MESSAGE BODY" to the end.

NOTE: the geo email is often abused (spoofed) by spammers.  We never send
encrypted messages or attachments unless agreed. We always sign emails by
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	geo@ncbi.nlm.nih.g[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606200076 ] ENA (Webin-24): file processing errors	[ Age: 14 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-20 06:02:02
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606190113 ] ENA (Webin-24): file processing errors	[ Age: 15 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-19 06:02:02
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606180081 ] ENA (Webin-24): file processing errors	[ Age: 16 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-18 06:02:02
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606170091 ] ENA (Webin-24): file processing errors	[ Age: 17 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-17 06:02:02
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606160799 ] [geo] GEO->AE unpublish notification: GSE69697 [NCBI trackin[..]	[ Age: 17 days 23 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-16 13:48:03
From:
"GEO - Emily Clough" <geo@ncbi.nlm.nih.gov>
To:
miamexpress@ebi.ac.uk
Subject:
[geo] GEO->AE unpublish notification: GSE69697 [NCBI tracking system #17936769[..]
------ MESSAGE BODY. YOU MAY CHANGE IT OR ADD COMMENTS ABOVE ------

Dear ArrayExpress Team,

The Series GSE69697 was returned to private status.

Regards,
The GEO Team
*************



---- END OF MESSAGE BODY.  PLEASE DO NOT CHANGE THE DATA BELOW ----
SK#:15:60:5:237:2924732

Please leave the subject line unchanged, and do not change the message
at end from the line with "END OF MESSAGE BODY" to the end.

[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	geo@ncbi.nlm.nih.g[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606160673 ] ENA (Webin-24): file processing errors	[ Age: 18 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-16 06:02:04
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606150531 ] [geo] GEO->AE unpublish notification: GSE54076 [NCBI trackin[..]	[ Age: 18 days 18 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-15 18:28:03
From:
"GEO - Patti Sherman" <geo@ncbi.nlm.nih.gov>
To:
miamexpress@ebi.ac.uk
Subject:
[geo] GEO->AE unpublish notification: GSE54076 [NCBI tracking system #17936045[..]
------ MESSAGE BODY. YOU MAY CHANGE IT OR ADD COMMENTS ABOVE ------

Dear ArrayExpress Team,

The Series GSE54076 was returned to private status.

Regards,
The GEO Team
*************


---- END OF MESSAGE BODY.  PLEASE DO NOT CHANGE THE DATA BELOW ----
SK#:15:60:5:222:122640

Please leave the subject line unchanged, and do not change the message
at end from the line with "END OF MESSAGE BODY" to the end.

NOTE: the geo email is often abused (spoofed) by spammers.  We never send
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	geo@ncbi.nlm.nih.g[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606150513 ] [geo] GEO->AE unpublish notification: GSE83333 [NCBI trackin[..]	[ Age: 18 days 20 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-15 15:56:03
From:
"GEO - Patti Sherman" <geo@ncbi.nlm.nih.gov>
To:
miamexpress@ebi.ac.uk
Subject:
[geo] GEO->AE unpublish notification: GSE83333 [NCBI tracking system #17935492[..]
------ MESSAGE BODY. YOU MAY CHANGE IT OR ADD COMMENTS ABOVE ------

Dear ArrayExpress Team,

The Series GSE83333 was returned to private status.

Regards,
The GEO Team
*************


---- END OF MESSAGE BODY.  PLEASE DO NOT CHANGE THE DATA BELOW ----
SK#:15:60:5:220:426540

Please leave the subject line unchanged, and do not change the message
at end from the line with "END OF MESSAGE BODY" to the end.

NOTE: the geo email is often abused (spoofed) by spammers.  We never send
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	geo@ncbi.nlm.nih.g[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606150184 ] ENA (Webin-24): file processing errors	[ Age: 19 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-15 06:06:03
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606140981 ] [geo] GEO->AE unpublish notification: GSE69770 [NCBI trackin[..]	[ Age: 19 days 18 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-14 18:40:10
From:
"GEO - Kimberly Marshall" <geo@ncbi.nlm.nih.gov>
To:
miamexpress@ebi.ac.uk
Subject:
[geo] GEO->AE unpublish notification: GSE69770 [NCBI tracking system #17934521[..]
------ MESSAGE BODY. YOU MAY CHANGE IT OR ADD COMMENTS ABOVE ------

Dear ArrayExpress Team,

The Series GSE69770 was returned to private status.

Regards,
The GEO Team
*************

---- END OF MESSAGE BODY.  PLEASE DO NOT CHANGE THE DATA BELOW ----
SK#:15:60:5:229:2192785

Please leave the subject line unchanged, and do not change the message
at end from the line with "END OF MESSAGE BODY" to the end.

NOTE: the geo email is often abused (spoofed) by spammers.  We never send
encrypted messages or attachments unless agreed. We always sign emails by
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	geo@ncbi.nlm.nih.g[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606140122 ] ENA (Webin-24): file processing errors	[ Age: 20 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-14 06:02:03
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606130357 ] [geo] GEO->AE unpublish notification: GSE75956 [NCBI trackin[..]	[ Age: 20 days 19 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-13 16:54:04
From:
"GEO - Patti Sherman" <geo@ncbi.nlm.nih.gov>
To:
miamexpress@ebi.ac.uk
Subject:
[geo] GEO->AE unpublish notification: GSE75956 [NCBI tracking system #17931818[..]
------ MESSAGE BODY. YOU MAY CHANGE IT OR ADD COMMENTS ABOVE ------

Dear ArrayExpress Team,

The Series GSE75956 was returned to private status.

Regards,
The GEO Team
*************


---- END OF MESSAGE BODY.  PLEASE DO NOT CHANGE THE DATA BELOW ----
SK#:15:60:5:232:84982

Please leave the subject line unchanged, and do not change the message
at end from the line with "END OF MESSAGE BODY" to the end.

NOTE: the geo email is often abused (spoofed) by spammers.  We never send
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	geo@ncbi.nlm.nih.g[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606130339 ] [geo] GEO->AE unpublish notification: GSE51636 [NCBI trackin[..]	[ Age: 20 days 20 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-13 16:18:03
From:
"GEO - Patti Sherman" <geo@ncbi.nlm.nih.gov>
To:
miamexpress@ebi.ac.uk
Subject:
[geo] GEO->AE unpublish notification: GSE51636 [NCBI tracking system #17931736[..]
------ MESSAGE BODY. YOU MAY CHANGE IT OR ADD COMMENTS ABOVE ------

Dear ArrayExpress Team,

The Series GSE51636 was returned to private status.

Regards,
The GEO Team
*************


---- END OF MESSAGE BODY.  PLEASE DO NOT CHANGE THE DATA BELOW ----
SK#:15:60:5:221:5205224

Please leave the subject line unchanged, and do not change the message
at end from the line with "END OF MESSAGE BODY" to the end.

NOTE: the geo email is often abused (spoofed) by spammers.  We never send
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	geo@ncbi.nlm.nih.g[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606130062 ] ENA (Webin-24): file processing errors	[ Age: 21 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-13 06:02:02
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606120064 ] ENA (Webin-24): file processing errors	[ Age: 22 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-12 06:02:03
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606110084 ] ENA (Webin-24): file processing errors	[ Age: 23 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-11 06:02:02
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606100273 ] [geo] GEO->AE unpublish notification: GSE75285, GSE75271, [..]	[ Age: 23 days 15 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-10 21:28:03
From:
"GEO - Irene Kim" <geo@ncbi.nlm.nih.gov>
To:
miamexpress@ebi.ac.uk
Subject:
[geo] GEO->AE unpublish notification: GSE75285, GSE75271, GSE75283, GSE75284 [[..]
------ MESSAGE BODY. YOU MAY CHANGE IT OR ADD COMMENTS ABOVE ------

Dear ArrayExpress Team,

The Series GSE75285, GSE75271, GSE75283, GSE75284 were returned to private status.

Regards,
The GEO Team
*************

---- END OF MESSAGE BODY.  PLEASE DO NOT CHANGE THE DATA BELOW ----
SK#:24:61:20:1:3097888

Please leave the subject line unchanged, and do not change the message
at end from the line with "END OF MESSAGE BODY" to the end.

NOTE: the geo email is often abused (spoofed) by spammers.  We never send
encrypted messages or attachments unless agreed. We always sign emails by
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	geo@ncbi.nlm.nih.g[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606100086 ] ENA (Webin-24): file processing errors	[ Age: 24 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-10 06:02:03
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606090311 ] [geo] GEO->AE unpublish notification: GSE78722 [NCBI trackin[..]	[ Age: 24 days 19 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-09 17:32:03
From:
"GEO - Carlos Evangelista" <geo@ncbi.nlm.nih.gov>
To:
miamexpress@ebi.ac.uk
Subject:
[geo] GEO->AE unpublish notification: GSE78722 [NCBI tracking system #17929395[..]
------ MESSAGE BODY. YOU MAY CHANGE IT OR ADD COMMENTS ABOVE ------

Dear ArrayExpress Team,

The Series GSE78722 was returned to private status.

Regards,
The GEO Team
*************

---- END OF MESSAGE BODY.  PLEASE DO NOT CHANGE THE DATA BELOW ----
SK#:15:60:5:226:5937297

Please leave the subject line unchanged, and do not change the message
at end from the line with "END OF MESSAGE BODY" to the end.

NOTE: the geo email is often abused (spoofed) by spammers.  We never send
encrypted messages or attachments unless agreed. We always sign emails by
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	geo@ncbi.nlm.nih.g[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606090258 ] Data withdrawal	[ Age: 24 days 22 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-09 14:16:04
From:
Quan Lin <ql3@sanger.ac.uk>
To:
arrayexpress <arrayexpress@ebi.ac.uk>
Cc:
Data submission service <datahose@sanger.ac.uk>
Subject:
Data withdrawal
Hello,

Could you please remove E-ERAD-465 from ArrayExpress as the linked data
in EGA has been withdrawn?


Thanks,
Quan



--
The Wellcome Trust Sanger Institute is operated by Genome Research
Limited, a charity registered in England with number 1021457 and a
company registered in England with number 2742969, whose registered
office is 215 Euston Road, London, NW1 2BE.
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	ql3@sanger.ac.uk
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606090098 ] ENA (Webin-24): file processing errors	[ Age: 25 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-09 06:02:03
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606080367 ] [geo] GEO->AE unpublish notification: GSE66041 [NCBI trackin[..]	[ Age: 25 days 20 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-08 15:52:07
From:
"GEO - Patti Sherman" <geo@ncbi.nlm.nih.gov>
To:
miamexpress@ebi.ac.uk
Subject:
[geo] GEO->AE unpublish notification: GSE66041 [NCBI tracking system #17927140[..]
------ MESSAGE BODY. YOU MAY CHANGE IT OR ADD COMMENTS ABOVE ------

Dear ArrayExpress Team,

The Series GSE66041 was returned to private status.

Regards,
The GEO Team
*************


---- END OF MESSAGE BODY.  PLEASE DO NOT CHANGE THE DATA BELOW ----
SK#:15:60:5:217:2784839

Please leave the subject line unchanged, and do not change the message
at end from the line with "END OF MESSAGE BODY" to the end.

NOTE: the geo email is often abused (spoofed) by spammers.  We never send
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	geo@ncbi.nlm.nih.g[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606080198 ] Data for ERA037246 is marked as 'paired-end' but loaded as [..]	[ Age: 26 days 2 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-08 10:08:03
From:
datasubs@ebi.ac.uk
To:
annotare@ebi.ac.uk
Subject:
Data for ERA037246 is marked as 'paired-end' but loaded as single-end (SUB#9189[..]
Dear Array Express colleagues,

Can you investigate the following?
E-MTAB-721/ERP000760/PRJEB2597

Thank you,
Marc

>Date: Tue, 7 Jun 2016 15:51:20 +0000
>From: jonathan.trow@nih.gov
>Reply-to:
>To: "datasubs@ebi.ac.uk" <datasubs@ebi.ac.uk>
>Subject: Data for ERA037246 is marked as 'paired-end' but loaded as single-end

> Dear Colleague,
> We received an inquiry about ERA037246 where some of the data (examples: ER=
> X014989, ERX014986) are indicated to be paired-end data, but dump as single=
> -end. It appears that matching forward and reverse reads were loaded to sep=
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606080171 ] ENA (Webin-24): file processing errors	[ Age: 26 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-08 06:02:03
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606080152 ] ENA (Webin-24): your data will become public in the next 14 [..]	[ Age: 26 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-08 06:02:02
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): your data will become public in the next 14 days
Dear Colleague,

We would like to inform you of your studies that will become public in the next 14 days
with all associated data.The list of studies is shown at the bottom of this email.If you
wish to extend the release date, please find the instructions in the following link:
http://www.ebi.ac.uk/ena/about/data-release-mechanism

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of studies nearing their publication date:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606070538 ] [geo] GEO->AE unpublish notification: GSE75443 [NCBI trackin[..]	[ Age: 26 days 19 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-07 16:52:06
From:
"GEO - Steve Wilhite" <geo@ncbi.nlm.nih.gov>
To:
miamexpress@ebi.ac.uk
Subject:
[geo] GEO->AE unpublish notification: GSE75443 [NCBI tracking system #17925213[..]
------ MESSAGE BODY. YOU MAY CHANGE IT OR ADD COMMENTS ABOVE ------

Dear ArrayExpress Team,

The Series GSE75443 was returned to private status.

Regards,
The GEO Team
*************


---- END OF MESSAGE BODY.  PLEASE DO NOT CHANGE THE DATA BELOW ----
SK#:15:60:5:223:6236982

Please leave the subject line unchanged, and do not change the message
at end from the line with "END OF MESSAGE BODY" to the end.

NOTE: the geo email is often abused (spoofed) by spammers.  We never send
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	geo@ncbi.nlm.nih.g[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606070341 ] [geo] GEO->AE unpublish notification: GSE58175 [NCBI trackin[..]	[ Age: 26 days 21 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-07 15:00:04
From:
"GEO - Steve Wilhite" <geo@ncbi.nlm.nih.gov>
To:
miamexpress@ebi.ac.uk
Subject:
[geo] GEO->AE unpublish notification: GSE58175 [NCBI tracking system #17925047[..]
------ MESSAGE BODY. YOU MAY CHANGE IT OR ADD COMMENTS ABOVE ------

Dear ArrayExpress Team,

The Series GSE58175 was returned to private status.

Regards,
The GEO Team
*************


---- END OF MESSAGE BODY.  PLEASE DO NOT CHANGE THE DATA BELOW ----
SK#:15:60:5:226:988891

Please leave the subject line unchanged, and do not change the message
at end from the line with "END OF MESSAGE BODY" to the end.

NOTE: the geo email is often abused (spoofed) by spammers.  We never send
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	geo@ncbi.nlm.nih.g[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606070065 ] ENA (Webin-24): file processing errors	[ Age: 27 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-07 06:02:03
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606060085 ] Data Files	[ Age: 28 days 0 hour ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-10 13:04:02
From:
datasubs@ebi.ac.uk
To:
arrayexpress@ebi.ac.uk
Subject:
Re: Data Files(rasko) (SUB#918814) [Ticket#1606060085]
Hi Ahmed,

> That would be great, thank you very much :)
>
> It really makes sense that cancelled data are no longer needed, but we have
> this case - and others - where the submitter decided to modify and re-arrange
> one or more experiments. In this specific case, he wants to split his study
> into 2 studies with different release dates! That's why we cancelled the
> project, and will submit two different submissions. But due to some migrations
> in the submission tool, many data files were deleted assuming that they were
> already brokered to ENA.
>
> Thanks for your help Rasko, I agree with your proposed solutions. Kindly make
> sure I have read access to these directories.

Done. There are ~250k new files which will gradually start showing up (will take
a bit of time for the changes to propagate to FIRE storage). Checked that one of
the two submitted fastqs is already available:
[...]
State:
open
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:
Owner:
ahmed
Trac:
Curation_Status:

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606060031 ] ENA (Webin-24): file processing errors	[ Age: 28 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-06 06:04:02
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606050041 ] ENA (Webin-24): file processing errors	[ Age: 29 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-05 06:02:03
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606030054 ] ENA (Webin-24): file processing errors	[ Age: 31 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-03 06:02:03
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1606010129 ] ENA (Webin-24): file processing errors	[ Age: 33 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-06-01 06:02:05
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move

[ Ticket#: 1605310164 ] ENA (Webin-24): file processing errors	[ Age: 34 days 6 hours ]
Lock - Zoom - History - Priority - Note - Close
Created:	2016-05-31 06:02:03
From:
"ENA" <datasubs@ebi.ac.uk>
To:
ArrayExpress submissions<annotare@ebi.ac.uk>
Subject:
ENA (Webin-24): file processing errors
Dear Colleague,

During processing of your submitted files, we have found problems with one or more of your
submitted files. Please review the error report provided at the end of this email and
re-upload corrected files to your upload area. We will automatically scan for these files
on a daily basis and attempt to re-process them.

This is an automatically generated email. If you wish to enquire about the contents of
this email, please reply to this email without any changes to the subject line.

Kind regards,
European Nucleotide Archive
European Molecular Biology Laboratory
European Bioinformatics Institute (EMBL-EBI),
Wellcome Trust Genome Campus, Hinxton, Cambridge CB10 1SD, U.K.
Tel: +44 1223 494444.

List of file processing errors:
[...]
State:
new
Priority:
3 normal
Queue:
developers::ahmed
CustomerID:	datasubs@ebi.ac.uk[..]
Owner:
root@localhost

Compose Answer (email):
Empty answer
Two-colour Annotare problem
Contact customer (phone):
Phone call
Change queue:
  Move
 Top of Page
Powered by OTRS 2.2.7

 """
    print ' '.join(geo_email_parse(email).keys())
