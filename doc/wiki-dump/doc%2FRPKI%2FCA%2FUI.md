# The CA user interface tools

The design of rpkid and pubd assumes that certain tasks can be thrown over the
wall to the registry's back end operation. This was a deliberate design
decision to allow rpkid and pubd to remain independent of existing database
schema, business PKIs, and so forth that a registry might already have. All
very nice, but it leaves someone who just wants to test the tools or who has
no existing back end with a fairly large programming project. The user
interface tools attempt to fill that gap. Together with irdbd, these tools
consitute the "IR back-end" (IRBE) programs.

[rpkic][1] is a command line interface to the the IRBE. The [web interface][2]
is a Django-based graphical user interface to the IRBE. The two user
interfaces are built on top of the same libraries, and can be used fairly
interchangeably. Most users will probably prefer the GUI, but the command line
interface may be useful for scripted control, for testing, or for environments
where running a web server is not practical.

A large registry which already has its own back-end system might want to roll
their own replacement for the entire IRBE package. The tools are designed to
allow this.

The user interface tools support two broad classes of operations:

  1. Relationship management: setting up relationships between RPKI parent and child entities and between publication repositories and their clients. This is primarily about exchange of BPKI keys with other entities and learning the service URLs at which rpkid should contact other servers. We refer to this as the "setup phase". 
  2. Operation of rpkid once relationships have been set up: issuing ROAs, assigning resources to children, and so forth. We refer to this as the "data maintenance" phase. 

During setup phase, the tools generate and processes small XML messages, which
they expects the user to ship to and from its parents, children, etc via some
out-of-band means (email, perhaps with PGP signatures, USB stick, we really
don't care). During data maintenance phase, the tools control the operation of
rpkid and pubd.

While the normal way to enter data during maintenance phase is by filling out
web forms, there's also a file-based format which can be used to upload and
download data from the GUI; the command line tool uses the same file format.
These files are simple whitespace-delimited text files (".csv files" -- the
name is historical, at one point these were parsed and generated using the
Python "csv" library, and the name stuck). The intent is that these be very
simple files that are easy to parse or to generate as a dump from relational
database, spreadsheet, awk script, whatever works in your environment.

As with rpkid and pubd, the user interface tools use a configuration file,
which defaults to the same system-wide rpki.conf file as the other programs.

## Overview of setup phase

While the specific commands one uses differ depending on whether you are using
the command line tool or the GUI, the basic operations during setup phase are
the same:

  1. If you haven't already done so, [install the software][3], create the [rpki.conf][4] for your installation, and [set up the MySQL database][5]. 
  2. If you haven't already done so, create the initial BPKI database for your installation by running the "rpkic initialize" command. This will also create a BPKI identity for the handle specified in your rpki.conf file. BPKI initialization is tied to creation of the initial BPKI identity for historical reasons. These operations probably ought to be handled by separate commands, and may be in the future. 
  3. If you haven't already done so, start the servers, using the `rpki-start-servers` script. 
  4. Send a copy of the XML identity file written out by "rpkic initialize" to each of your parents, somehow (email, USB stick, carrier pigeon, we don't care). The XML identity file will have a filename like ./${handle}.identity.xml where "." is the directory in which you ran rpkic and ${handle} is the handle set in your rpki.conf file or selected with rpkic's `select_identity` command. This XML identity file tells each of your parents what you call yourself, and supplies each parent with a trust anchor for your resource-holding BPKI. 
  5. Each of your parents configures you as a child, using the XML identity file you supplied as input. This registers your data with the parent, including BPKI cross-registration, and generates a return message containing your parent's BPKI trust anchors, a service URL for contacting your parent via the "up-down" protocol, and (usually) either an offer of publication service (if your parent operates a repository) or a referral from your parent to whatever publication service your parent does use. Referrals include a CMS-signed authorization token that the repository operator can use to determine that your parent has given you permission to home underneath your parent in the publication tree. 
  6. Each of your parents sends (...) back the response XML file generated by the "configure_child" command. 
  7. You feed the response message you just got into the IRBE using rpkic's "configure_parent" command. This registers the parent's information in your database, handles BPKI cross-certification of your parent., and processes the repository offer or referral to generate a publication request message. 
  8. You send (...) the publication request message to the repository. The `contact_info` element in the request message should (in theory) provide some clue as to where you should send this. 
  9. The repository operator processes your request using rpkic's "configure_publication_client" command. This registers your information, including BPKI cross-certification, and generates a response message containing the repository's BPKI trust anchor and service URL. 
  10. Repository operator sends (...) the publication confirmation message back to you. 
  11. You process the publication confirmation message using rpkic's "configure_repository" command. 

At this point you should, in theory, have established relationships, exchanged
trust anchors, and obtained service URLs from all of your parents and
repositories.

## Troubleshooting

If you run into trouble setting up this package, the first thing to do is
categorize the kind of trouble you are having. If you've gotten far enough to
be running the daemons, check their log files. If you're seeing Python
exceptions, read the error messages. If you're getting CMS errors, check to
make sure that you're using all the right BPKI certificates and service
contact URLs.

If you've completed the steps above, everything appears to have gone OK, but
nothing seems to be happening, the first thing to do is check the logs to
confirm that nothing is actively broken. rpkid's log should include messages
telling you when it starts and finishes its internal "cron" cycle. It can take
several cron cycles for resources to work their way down from your parent into
a full set of certificates and ROAs, so have a little patience. rpkid's log
should also include messages showing every time it contacts its parent(s) or
attempts to publish anything.

rcynic in fully verbose mode provides a fairly detailed explanation of what
it's doing and why objects that fail have failed.

You can use rsync (sic) to examine the contents of a publication repository
one directory at a time, without attempting validation, by running rsync with
just the URI of the directory on its command line:

    
    
    $ rsync rsync://rpki.example.org/where/ever/
    

If you need to examine RPKI objects in detail, you have a few options:

  * The [RPKI utilities][6] include several programs for dumping RPKI-specific objects in text form. 
  * The OpenSSL command line program can also be useful for examining and manipulating certificates and CMS messages, although the syntax of some of the commands can be a bit obscure. 
  * Peter Gutmann's excellent [dumpasn1][7] program may be useful if you are desperate enough that you need to examine raw ASN.1 objects. 

   [1]: #_.wiki.doc.RPKI.CA.UI.rpkic

   [2]: #_.wiki.doc.RPKI.CA.UI.GUI

   [3]: #_.wiki.doc.RPKI.Installation

   [4]: #_.wiki.doc.RPKI.CA.Configuration

   [5]: #_.wiki.doc.RPKI.CA.MySQLSetup

   [6]: #_.wiki.doc.RPKI.Utils

   [7]: http://www.cs.auckland.ac.nz/~pgut001/dumpasn1.c

